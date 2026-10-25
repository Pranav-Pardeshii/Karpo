import React, { useState, useEffect, useRef } from "react";
import { Mic, MicOff, Volume2, VolumeX, Send, X, MessageSquare, AlertCircle, Sparkles } from "lucide-react";
import { api } from "../api/client";
import { VoiceQueryResponse } from "../types/api";

// Web Speech API interface declarations
interface IWindow extends Window {
  SpeechRecognition?: any;
  webkitSpeechRecognition?: any;
}

export const KisanVoiceAssistant: React.FC = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [language, setLanguage] = useState<string>("mr"); // Default to Marathi
  const [isListening, setIsListening] = useState<boolean>(false);
  const [inputText, setInputText] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [response, setResponse] = useState<VoiceQueryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [ttsEnabled, setTtsEnabled] = useState<boolean>(true);

  const recognitionRef = useRef<any>(null);

  // Initialize Speech Recognition if supported by the browser
  useEffect(() => {
    const customWindow = window as unknown as IWindow;
    const SpeechRec = customWindow.SpeechRecognition || customWindow.webkitSpeechRecognition;

    if (SpeechRec) {
      const recognition = new SpeechRec();
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onstart = () => {
        setIsListening(true);
        setError(null);
      };

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setInputText(transcript);
        setIsListening(false);
        handleSendQuery(transcript, language);
      };

      recognition.onerror = (event: any) => {
        setIsListening(false);
        if (event.error === "not-allowed") {
          setError("Microphone permission denied. You can type your query below.");
        } else if (event.error === "no-speech") {
          setError("No voice detected. Please try speaking again or type below.");
        } else {
          setError(`Speech input issue (${event.error}). Please type your query.`);
        }
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    }
  }, []);

  // Update recognition language when user changes selection
  useEffect(() => {
    if (recognitionRef.current) {
      const langMap: Record<string, string> = {
        mr: "mr-IN",
        hi: "hi-IN",
        en: "en-IN",
      };
      recognitionRef.current.lang = langMap[language] || "en-IN";
    }
  }, [language]);

  const toggleListening = () => {
    if (!recognitionRef.current) {
      setError("Voice input is not supported in this browser. Please use text input.");
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      setError(null);
      try {
        recognitionRef.current.start();
      } catch {
        recognitionRef.current.stop();
        setTimeout(() => recognitionRef.current.start(), 200);
      }
    }
  };

  const speakText = (text: string, lang: string) => {
    if (!ttsEnabled || !window.speechSynthesis) return;

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    const langMap: Record<string, string> = {
      mr: "mr-IN",
      hi: "hi-IN",
      en: "en-IN",
    };
    utterance.lang = langMap[lang] || "en-IN";
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
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
      handleSendQuery(inputText, language);
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
            className="flex items-center gap-2.5 px-4 py-3 bg-obsidian-950 hover:bg-obsidian-900 border-2 border-signal-red text-chalk-100 shadow-brutal transition-all group"
            title="Open Kisan Voice Assistant"
          >
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-signal-red opacity-75" />
              <span className="relative inline-flex rounded-full h-3 w-3 bg-signal-red" />
            </span>
            <Mic className="w-4 h-4 text-signal-red group-hover:scale-110 transition-transform" />
            <span className="font-mono text-xs font-bold uppercase tracking-wider">
              Kisan Copilot
            </span>
          </button>
        )}
      </div>

      {/* Assistant Modal / Drawer */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 z-50 w-[92vw] sm:w-[420px] bg-obsidian-950 border-2 border-obsidian-700 shadow-brutal flex flex-col max-h-[85vh] print:hidden">
          {/* Header */}
          <div className="p-4 border-b border-obsidian-800 flex items-center justify-between bg-obsidian-900">
            <div className="flex items-center gap-2">
              <div className="p-1.5 bg-signal-red/10 border border-signal-red/30">
                <Mic className="w-4 h-4 text-signal-red" />
              </div>
              <div>
                <h3 className="font-mono text-xs font-bold uppercase tracking-wider text-chalk-100">
                  Kisan Voice Copilot
                </h3>
                <span className="text-[10px] font-mono text-obsidian-400 block">
                  Vernacular Agricultural Voice Assistant
                </span>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => {
                  setTtsEnabled(!ttsEnabled);
                  if (ttsEnabled && window.speechSynthesis) {
                    window.speechSynthesis.cancel();
                  }
                }}
                className="p-1.5 text-obsidian-400 hover:text-chalk-100 transition-colors"
                title={ttsEnabled ? "Mute Voice Playback" : "Enable Voice Playback"}
              >
                {ttsEnabled ? <Volume2 className="w-4 h-4 text-emerald-400" /> : <VolumeX className="w-4 h-4" />}
              </button>

              <button
                type="button"
                onClick={() => {
                  setIsOpen(false);
                  if (window.speechSynthesis) window.speechSynthesis.cancel();
                  if (isListening && recognitionRef.current) recognitionRef.current.stop();
                }}
                className="p-1.5 text-obsidian-400 hover:text-chalk-100 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Language Selector */}
          <div className="px-4 py-2 border-b border-obsidian-800 bg-obsidian-950 flex items-center justify-between text-xs font-mono">
            <span className="text-[11px] text-obsidian-400">Language:</span>
            <div className="flex items-center gap-1.5">
              {[
                { code: "mr", label: "मराठी" },
                { code: "hi", label: "हिंदी" },
                { code: "en", label: "English" },
              ].map((lang) => (
                <button
                  key={lang.code}
                  type="button"
                  onClick={() => setLanguage(lang.code)}
                  className={`px-2.5 py-1 text-xs transition-colors border ${
                    language === lang.code
                      ? "border-signal-red bg-signal-red/10 text-white font-bold"
                      : "border-obsidian-800 bg-obsidian-900 text-obsidian-400 hover:text-chalk-200"
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
              <span className="text-[10px] text-obsidian-500 uppercase tracking-widest flex items-center gap-1">
                <Sparkles className="w-3 h-3 text-signal-red" />
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
                    className="px-2 py-1 bg-obsidian-900 hover:bg-obsidian-850 text-obsidian-300 hover:text-chalk-100 border border-obsidian-800 text-[11px] transition-colors text-left"
                  >
                    {chip}
                  </button>
                ))}
              </div>
            </div>

            {/* Error Banner */}
            {error && (
              <div className="p-2.5 bg-signal-red/10 border border-signal-red/30 text-signal-red text-xs flex items-center gap-2">
                <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {/* Listening Indicator */}
            {isListening && (
              <div className="p-4 bg-obsidian-900 border border-signal-red text-center space-y-2 animate-pulse">
                <div className="w-8 h-8 rounded-full bg-signal-red text-white mx-auto flex items-center justify-center">
                  <Mic className="w-4 h-4 animate-bounce" />
                </div>
                <div className="text-xs font-bold text-chalk-100">
                  {language === "mr" ? "ऐकत आहे... बोला" : language === "hi" ? "सुन रहा हूँ... बोलिए" : "Listening... Speak now"}
                </div>
                <span className="text-[10px] text-obsidian-400">
                  {language === "mr" ? "मराठी भाषेत प्रश्न विचारा" : language === "hi" ? "हिंदी में पूछें" : "Ask in English"}
                </span>
              </div>
            )}

            {/* Response Card */}
            {response && (
              <div className="p-3.5 bg-obsidian-900 border border-obsidian-800 space-y-2.5">
                <div className="flex items-center justify-between pb-1.5 border-b border-obsidian-800">
                  <span className="text-[10px] uppercase font-bold text-emerald-400 flex items-center gap-1">
                    <MessageSquare className="w-3 h-3" />
                    {response.intent.replace("_", " ")}
                  </span>
                  <span className="text-[9px] px-1.5 py-0.5 bg-obsidian-800 text-obsidian-300 border border-obsidian-700">
                    {response.data_category}
                  </span>
                </div>

                <p className="text-xs text-chalk-100 font-sans leading-relaxed">
                  {response.display_text}
                </p>

                {/* Structured Data Highlights */}
                {response.structured_data && response.intent === "market_price" && (
                  <div className="grid grid-cols-2 gap-2 pt-1 font-mono text-[11px]">
                    <div className="p-2 bg-obsidian-950 border border-obsidian-800">
                      <span className="text-[9px] text-obsidian-400 block">Modal Rate:</span>
                      <span className="font-bold text-chalk-100">
                        ₹{response.structured_data.modal_rs_per_quintal?.toLocaleString()} / Q
                      </span>
                    </div>
                    {response.structured_data.msp_rs_per_quintal && (
                      <div className="p-2 bg-obsidian-950 border border-obsidian-800">
                        <span className="text-[9px] text-obsidian-400 block">Govt MSP:</span>
                        <span className="font-bold text-emerald-400">
                          ₹{response.structured_data.msp_rs_per_quintal?.toLocaleString()} / Q
                        </span>
                      </div>
                    )}
                  </div>
                )}

                <div className="pt-1.5 border-t border-obsidian-800/80 flex items-center justify-between text-[10px] text-obsidian-500">
                  <span>Source: {response.data_provenance}</span>
                  {ttsEnabled && (
                    <button
                      type="button"
                      onClick={() => speakText(response.spoken_text, response.language)}
                      className="text-signal-red hover:underline flex items-center gap-1 font-bold"
                    >
                      <Volume2 className="w-3 h-3" /> Replay
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Input Bar */}
          <form onSubmit={handleSubmit} className="p-3 border-t border-obsidian-800 bg-obsidian-900 flex items-center gap-2">
            <button
              type="button"
              onClick={toggleListening}
              className={`p-2.5 border transition-all shrink-0 ${
                isListening
                  ? "bg-signal-red text-white border-signal-red animate-pulse"
                  : "bg-obsidian-950 hover:bg-obsidian-850 text-chalk-200 border-obsidian-750"
              }`}
              title={isListening ? "Stop Listening" : "Start Voice Input"}
            >
              {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4 text-signal-red" />}
            </button>

            <input
              type="text"
              placeholder={
                language === "mr"
                  ? "बोलून किंवा टाईप करून विचारा..."
                  : language === "hi"
                  ? "बोलें या टाइप करके पूछें..."
                  : "Speak or type your question..."
              }
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              className="flex-1 bg-obsidian-950 border border-obsidian-750 text-chalk-100 px-3 py-2 text-xs font-mono focus:border-signal-red focus:outline-none placeholder:text-obsidian-500"
            />

            <button
              type="submit"
              disabled={loading || !inputText.trim()}
              className="p-2.5 bg-signal-red hover:bg-red-600 text-white border border-signal-red disabled:opacity-40 transition-colors shrink-0"
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
