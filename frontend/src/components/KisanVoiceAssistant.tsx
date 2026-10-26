import React, { useState, useEffect, useRef } from "react";
import { Mic, MicOff, Volume2, VolumeX, Send, X, MessageSquare, AlertCircle, Sparkles, Loader2 } from "lucide-react";
import { api } from "../api/client";
import { VoiceQueryResponse } from "../types/api";

interface IWindow extends Window {
  SpeechRecognition?: any;
  webkitSpeechRecognition?: any;
}

const sanitizeVoiceText = (text: string): string => {
  return text
    .replace(/\bmandi\s*p\s*rice\b/gi, "mandi price")
    .replace(/\bmandip\s*rice\b/gi, "mandi price")
    .replace(/\bmarket\s*p\s*rice\b/gi, "market price")
    .replace(/\bcrop\s*p\s*rice\b/gi, "crop price")
    .replace(/\bcost\s*p\s*rice\b/gi, "cost price");
};

export const KisanVoiceAssistant: React.FC = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [language, setLanguage] = useState<string>("mr"); // Default to Marathi
  const [isListening, setIsListening] = useState<boolean>(false);
  const [isTranscribing, setIsTranscribing] = useState<boolean>(false);
  const [inputText, setInputText] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [response, setResponse] = useState<VoiceQueryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [ttsEnabled, setTtsEnabled] = useState<boolean>(true);
  const [isPlayingAudio, setIsPlayingAudio] = useState<boolean>(false);

  // Audio & MediaRecorder refs
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const streamRef = useRef<MediaStream | null>(null);
  const autoStopTimeoutRef = useRef<number | null>(null);
  const currentAudioRef = useRef<HTMLAudioElement | null>(null);

  // Web Speech fallback ref
  const webSpeechRecognitionRef = useRef<any>(null);

  // Clean up recording streams and audio playback on unmount
  useEffect(() => {
    return () => {
      if (autoStopTimeoutRef.current) clearTimeout(autoStopTimeoutRef.current);
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
      if (currentAudioRef.current) {
        currentAudioRef.current.pause();
      }
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  // Initialize Web Speech API as fallback for browsers that prefer it
  useEffect(() => {
    const customWindow = window as unknown as IWindow;
    const SpeechRec = customWindow.SpeechRecognition || customWindow.webkitSpeechRecognition;

    if (SpeechRec) {
      try {
        const recognition = new SpeechRec();
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {
          setIsListening(true);
          setError(null);
        };

        recognition.onresult = (event: any) => {
          const transcript = sanitizeVoiceText(event.results[0][0].transcript);
          setInputText(transcript);
          setIsListening(false);
          handleSendQuery(transcript, language);
        };

        recognition.onerror = (event: any) => {
          setIsListening(false);
          if (event.error === "network") {
            // Brave blocks google speech-api; start MediaRecorder + Groq Whisper
            startMediaRecording();
          } else if (event.error === "not-allowed") {
            setError("Microphone permission denied. Please allow microphone access in your browser or type your query below.");
          } else if (event.error === "no-speech") {
            setError("No voice detected. Please try speaking again or type below.");
          } else {
            setError(`Speech input issue (${event.error}). Please type your query.`);
          }
        };

        recognition.onend = () => {
          setIsListening(false);
        };

        webSpeechRecognitionRef.current = recognition;
      } catch {
        webSpeechRecognitionRef.current = null;
      }
    }
  }, [language]);

  // Start direct MediaRecorder and transcribe using Groq Whisper (Brave-friendly, 0 cloud-telemetry blocks)
  const startMediaRecording = async () => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      setError("Microphone input is not supported by your browser. Please type your query below.");
      return;
    }

    setError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      let mimeType = "audio/webm";
      if (!MediaRecorder.isTypeSupported("audio/webm")) {
        if (MediaRecorder.isTypeSupported("audio/mp4")) {
          mimeType = "audio/mp4";
        } else if (MediaRecorder.isTypeSupported("audio/ogg")) {
          mimeType = "audio/ogg";
        } else {
          mimeType = "";
        }
      }

      const recorder = mimeType ? new MediaRecorder(stream, { mimeType }) : new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;
      audioChunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      recorder.onstop = async () => {
        setIsListening(false);
        if (streamRef.current) {
          streamRef.current.getTracks().forEach((track) => track.stop());
          streamRef.current = null;
        }

        const recordedBlob = new Blob(audioChunksRef.current, {
          type: recorder.mimeType || "audio/webm",
        });

        if (recordedBlob.size < 500) {
          setError("No clear audio captured. Please speak closer to your microphone or type below.");
          return;
        }

        setIsTranscribing(true);
        try {
          const extension = recorder.mimeType.includes("mp4")
            ? "mp4"
            : recorder.mimeType.includes("ogg")
            ? "ogg"
            : "webm";
          const formData = new FormData();
          formData.append(
            "file",
            new File([recordedBlob], `recording.${extension}`, { type: recordedBlob.type })
          );

          const transcriptRes = await api.transcribeAudio(formData, language);
          const recognizedText = sanitizeVoiceText(transcriptRes.text.trim());

          if (recognizedText) {
            setInputText(recognizedText);
            handleSendQuery(recognizedText, language);
          } else {
            setError("No speech was recognized. Please speak clearly or type your query.");
          }
        } catch (transcribeErr: any) {
          setError(
            transcribeErr?.message || "Speech transcription failed. Please try again or type below."
          );
        } finally {
          setIsTranscribing(false);
        }
      };

      recorder.start(250);
      setIsListening(true);

      // Auto stop after 9 seconds of speech
      if (autoStopTimeoutRef.current) clearTimeout(autoStopTimeoutRef.current);
      autoStopTimeoutRef.current = window.setTimeout(() => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
          mediaRecorderRef.current.stop();
        }
      }, 9000);
    } catch (micErr: any) {
      setIsListening(false);
      if (micErr.name === "NotAllowedError" || micErr.name === "PermissionDeniedError") {
        setError(
          "Microphone permission denied. Please allow microphone access in your browser bar, or type your query below."
        );
      } else {
        setError(`Microphone error: ${micErr.message || "Unable to access microphone"}. Please type below.`);
      }
    }
  };

  const stopMediaRecording = () => {
    if (autoStopTimeoutRef.current) clearTimeout(autoStopTimeoutRef.current);
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      mediaRecorderRef.current.stop();
    }
    if (webSpeechRecognitionRef.current) {
      try {
        webSpeechRecognitionRef.current.stop();
      } catch {
        // Ignore stop on unstarted recognition
      }
    }
    setIsListening(false);
  };

  const toggleListening = () => {
    if (isListening) {
      stopMediaRecording();
    } else {
      // Prioritize MediaRecorder + Groq Whisper to prevent Brave/network speech-api errors
      startMediaRecording();
    }
  };

  const fallbackToWebSpeech = (text: string, lang: string) => {
    if (!ttsEnabled || !window.speechSynthesis) {
      setIsPlayingAudio(false);
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    const langMap: Record<string, string> = {
      mr: "mr-IN",
      hi: "hi-IN",
      en: "en-IN",
    };
    utterance.lang = langMap[lang] || "en-IN";
    utterance.rate = 0.95;
    utterance.onend = () => setIsPlayingAudio(false);
    utterance.onerror = () => setIsPlayingAudio(false);
    window.speechSynthesis.speak(utterance);
  };

  const speakText = async (text: string, lang: string) => {
    if (!ttsEnabled) return;

    // Stop any currently playing audio or speech
    if (currentAudioRef.current) {
      currentAudioRef.current.pause();
      currentAudioRef.current = null;
    }
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }

    setIsPlayingAudio(true);

    try {
      // 1. Try ElevenLabs studio audio synthesis from backend
      const audioBlob = await api.synthesizeSpeech(text, lang);
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      currentAudioRef.current = audio;

      audio.onended = () => {
        setIsPlayingAudio(false);
        URL.revokeObjectURL(audioUrl);
      };

      audio.onerror = () => {
        setIsPlayingAudio(false);
        fallbackToWebSpeech(text, lang);
      };

      await audio.play();
    } catch (elevenLabsErr) {
      console.warn("ElevenLabs TTS unavailable, falling back to Web Speech API:", elevenLabsErr);
      fallbackToWebSpeech(text, lang);
    }
  };

  const handleSendQuery = async (query: string, lang: string) => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const res = await api.queryVoiceCopilot({
        query_text: query.trim(),
        language: lang,
        state: "Maharashtra",
      });
      setResponse(res);
      speakText(res.spoken_text, res.language);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Unable to reach voice advisory server.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputText.trim()) {
      const sanitized = sanitizeVoiceText(inputText);
      setInputText(sanitized);
      handleSendQuery(sanitized, language);
    }
  };

  const suggestionChips = {
    mr: ["सोयाबीनचा भाव काय आहे?", "कापूस लागवड खर्च", "भातासाठी खताचा सल्ला"],
    hi: ["सोयाबीन का मंडी भाव", "कपास की खेती लागत", "गेहूं बुवाई सलाह"],
    en: ["Wheat mandi price", "Cotton cultivation cost", "Rice soil advisory"],
  }[language] || ["Wheat price", "Cotton cost", "Rice soil"];

  return (
    <>
      {/* Floating Launcher Button */}
      <div className="fixed bottom-6 right-6 z-50 print:hidden">
        {!isOpen && (
          <button
            type="button"
            onClick={() => setIsOpen(true)}
            className="flex items-center gap-2.5 px-4 py-2.5 bg-white hover:bg-obsidian-850 border border-signal-red text-signal-red shadow-md transition-all group"
            title="Open Kisan Voice Assistant"
          >
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-signal-lime opacity-75" />
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-signal-red" />
            </span>
            <Mic className="w-4 h-4 text-signal-red group-hover:scale-110 transition-transform" />
            <span className="font-mono text-xs font-bold uppercase tracking-wider text-chalk-100">
              Kisan Copilot
            </span>
          </button>
        )}
      </div>

      {/* Assistant Modal / Drawer */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 z-50 w-[92vw] sm:w-[420px] bg-white border border-obsidian-800 shadow-xl flex flex-col max-h-[85vh] print:hidden">
          {/* Header */}
          <div className="p-4 border-b border-obsidian-800 flex items-center justify-between bg-obsidian-850">
            <div className="flex items-center gap-2">
              <div className="p-1.5 bg-white border border-signal-red/30 text-signal-red">
                <Mic className="w-4 h-4" />
              </div>
              <div>
                <h3 className="font-mono text-xs font-bold uppercase tracking-wider text-chalk-100">
                  Kisan Voice Copilot
                </h3>
                <p className="text-[10px] text-obsidian-400">
                  Vernacular Agricultural Voice Assistant
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setTtsEnabled(!ttsEnabled)}
                className={`p-1.5 border transition-colors ${
                  ttsEnabled
                    ? "text-signal-red border-signal-red/30 bg-white"
                    : "text-obsidian-400 border-obsidian-800 bg-obsidian-850"
                }`}
                title={ttsEnabled ? "Text-to-speech audio active" : "Audio muted"}
              >
                {ttsEnabled ? <Volume2 className="w-3.5 h-3.5" /> : <VolumeX className="w-3.5 h-3.5" />}
              </button>

              <button
                type="button"
                onClick={() => setIsOpen(false)}
                className="p-1.5 text-obsidian-400 hover:text-chalk-100 hover:bg-white transition-colors"
                title="Close Assistant"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Language Selector */}
          <div className="px-4 py-2 bg-white border-b border-obsidian-800 flex items-center justify-between text-xs">
            <span className="text-[11px] text-obsidian-400 font-mono">Language:</span>
            <div className="flex items-center gap-1">
              {[
                { code: "mr", label: "मराठी" },
                { code: "hi", label: "हिंदी" },
                { code: "en", label: "English" },
              ].map((lang) => (
                <button
                  key={lang.code}
                  type="button"
                  onClick={() => setLanguage(lang.code)}
                  className={`px-2 py-0.5 text-xs font-mono transition-colors border ${
                    language === lang.code
                      ? "bg-signal-red text-white border-signal-red font-bold"
                      : "bg-obsidian-850 text-obsidian-400 border-obsidian-800 hover:bg-[#DCE6D7]"
                  }`}
                >
                  {lang.label}
                </button>
              ))}
            </div>
          </div>

          {/* Chat / Responses Area */}
          <div className="p-4 overflow-y-auto space-y-4 flex-1 font-mono text-xs max-h-[350px]">
            {/* Quick Suggestion Chips */}
            <div className="space-y-1.5">
              <span className="text-[10px] text-obsidian-400 uppercase tracking-widest flex items-center gap-1 font-semibold">
                <Sparkles className="w-3 h-3 text-signal-lime" />
                Quick Questions
              </span>
              <div className="flex flex-wrap gap-1.5">
                {suggestionChips.map((chip, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => {
                      setInputText(chip);
                      handleSendQuery(chip, language);
                    }}
                    className="px-2 py-1 bg-obsidian-850 hover:bg-[#DCE6D7] text-chalk-100 border border-obsidian-800 text-[11px] transition-colors text-left"
                  >
                    {chip}
                  </button>
                ))}
              </div>
            </div>

            {/* Error Banner */}
            {error && (
              <div className="p-2.5 bg-[#FDF2F2] border border-signal-error/40 text-signal-error text-xs flex items-center gap-2">
                <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                <span className="leading-snug">{error}</span>
              </div>
            )}

            {/* Listening Indicator */}
            {isListening && (
              <div className="p-4 bg-obsidian-850 border border-signal-red text-center space-y-2 shadow-sm">
                <div className="w-8 h-8 rounded-full bg-signal-red text-white font-bold mx-auto flex items-center justify-center">
                  <Mic className="w-4 h-4 animate-bounce" />
                </div>
                <div className="text-xs font-bold text-chalk-100">
                  {language === "mr"
                    ? "ऐकत आहे... बोला (थांबवण्यासाठी माईक पुन्हा दाबा)"
                    : language === "hi"
                    ? "सुन रहा हूँ... बोलिए (रोकने के लिए माइक दबाएं)"
                    : "Listening... Speak now (Click mic when done)"}
                </div>
                <span className="text-[10px] text-obsidian-400">
                  Powered by Groq Whisper STT &bull; Privacy friendly
                </span>
              </div>
            )}

            {/* Transcribing Indicator */}
            {isTranscribing && (
              <div className="p-3 bg-[#FDF8F0] border border-signal-amber/40 text-center space-y-2">
                <div className="w-7 h-7 rounded-full bg-signal-amber/10 text-signal-amber mx-auto flex items-center justify-center">
                  <Loader2 className="w-4 h-4 animate-spin" />
                </div>
                <div className="text-xs font-bold text-signal-amber">
                  {language === "mr"
                    ? "आवाज ओळखत आहे (Groq Whisper)..."
                    : language === "hi"
                    ? "आवाज़ पहचानी जा रही है (Groq Whisper)..."
                    : "Transcribing audio via Groq Whisper..."}
                </div>
              </div>
            )}

            {/* Response Card */}
            {response && (
              <div className="p-3.5 bg-obsidian-850 border border-obsidian-800 space-y-2.5">
                <div className="flex items-center justify-between pb-1.5 border-b border-obsidian-800">
                  <span className="text-[10px] uppercase font-bold text-signal-red flex items-center gap-1">
                    <MessageSquare className="w-3 h-3" />
                    {response.intent.replace("_", " ")}
                  </span>
                  <span className="text-[9px] px-1.5 py-0.5 bg-white text-obsidian-400 border border-obsidian-800">
                    {response.data_category}
                  </span>
                </div>

                <p className="text-xs text-chalk-100 font-sans leading-relaxed">
                  {response.display_text}
                </p>

                {/* Structured Data Highlights */}
                {response.structured_data && response.intent === "market_price" && (
                  <div className="grid grid-cols-2 gap-2 pt-1 font-mono text-[11px]">
                    <div className="p-2 bg-white border border-obsidian-800">
                      <span className="text-[9px] text-obsidian-400 block">Modal Rate:</span>
                      <span className="font-bold text-chalk-100">
                        ₹{response.structured_data.modal_rs_per_quintal?.toLocaleString()} / Q
                      </span>
                    </div>
                    {response.structured_data.msp_rs_per_quintal && (
                      <div className="p-2 bg-white border border-obsidian-800">
                        <span className="text-[9px] text-obsidian-400 block">Govt MSP:</span>
                        <span className="font-bold text-signal-red">
                          ₹{response.structured_data.msp_rs_per_quintal?.toLocaleString()} / Q
                        </span>
                      </div>
                    )}
                  </div>
                )}

                <div className="pt-1.5 border-t border-obsidian-800 flex items-center justify-between text-[10px] text-obsidian-400">
                  <span>Source: {response.data_provenance}</span>
                  {ttsEnabled && (
                    <button
                      type="button"
                      onClick={() => speakText(response.spoken_text, response.language)}
                      disabled={isPlayingAudio}
                      className="text-signal-red hover:underline flex items-center gap-1 font-bold disabled:opacity-60 cursor-pointer"
                    >
                      <Volume2 className={`w-3 h-3 ${isPlayingAudio ? "animate-bounce text-signal-lime" : ""}`} />
                      {isPlayingAudio ? "Playing (ElevenLabs)..." : "Replay"}
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Input Bar */}
          <form onSubmit={handleSubmit} className="p-3 border-t border-obsidian-800 bg-white flex items-center gap-2">
            <button
              type="button"
              onClick={toggleListening}
              disabled={isTranscribing}
              className={`p-2.5 border transition-all shrink-0 cursor-pointer ${
                isListening
                  ? "bg-signal-red text-white font-bold border-signal-red shadow-sm"
                  : isTranscribing
                  ? "bg-[#FDF8F0] text-signal-amber border-signal-amber/40"
                  : "bg-obsidian-850 hover:bg-[#DCE6D7] text-signal-red border-obsidian-800"
              }`}
              title={isListening ? "Stop and transcribe" : "Click to speak"}
            >
              {isListening ? (
                <MicOff className="w-4 h-4" />
              ) : isTranscribing ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Mic className="w-4 h-4 text-signal-red" />
              )}
            </button>

            <input
              type="text"
              placeholder={
                isListening
                  ? language === "mr"
                    ? "माईकमध्ये बोला..."
                    : language === "hi"
                    ? "माइक में बोलें..."
                    : "Speaking into microphone..."
                  : isTranscribing
                  ? "Transcribing with Groq Whisper..."
                  : language === "mr"
                  ? "बोलून किंवा टाईप करून विचारा..."
                  : language === "hi"
                  ? "बोलें या टाइप करके पूछें..."
                  : "Speak or type your question..."
              }
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              className="flex-1 bg-white border border-obsidian-800 text-chalk-100 px-3 py-2 text-xs font-mono focus:border-signal-red focus:outline-none placeholder:text-obsidian-400"
            />

            <button
              type="submit"
              disabled={loading || isTranscribing || !inputText.trim()}
              className="p-2.5 bg-signal-red hover:bg-signal-darkred text-white font-bold border border-signal-red shadow-sm disabled:opacity-40 transition-all shrink-0 cursor-pointer"
              title="Submit query"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      )}
    </>
  );
};
