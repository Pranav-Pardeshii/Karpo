import React, { useState, useRef } from "react";
import {
  Camera,
  Upload,
  UploadCloud,
  AlertCircle,
  ShieldAlert,
  CheckCircle,
  FileText,
  RefreshCw,
  Info,
  AlertTriangle,
} from "lucide-react";
import { api } from "../api/client";
import { LensInspectionResponse } from "../types/api";

export const KarpoLens: React.FC = () => {
  const [selectedCrop, setSelectedCrop] = useState<string>("rice");
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [inspectionResult, setInspectionResult] = useState<LensInspectionResponse | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const processSelectedFile = (file: File) => {
    if (!file.type.startsWith("image/")) {
      setError("Please provide a valid image file (JPEG, PNG, or WEBP).");
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError("Image size exceeds the maximum limit of 10 MB.");
      return;
    }

    setSelectedFile(file);
    setError(null);
    setInspectionResult(null);

    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      processSelectedFile(file);
    }
  };

  // Drag and Drop Event Handlers
  const handleDragEnter = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (!isDragging) setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    // Only set dragging false if leaving the current target
    if (e.currentTarget.contains(e.relatedTarget as Node)) return;
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      processSelectedFile(files[0]);
    }
  };

  const handleUploadAndInspect = async () => {
    if (!selectedFile) {
      setError("Please drop or select a leaf photo first.");
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("image", selectedFile);
    formData.append("crop", selectedCrop);

    try {
      const res = await api.inspectCropImage(formData);
      setInspectionResult(res);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Image inspection failed.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setInspectionResult(null);
    setError(null);
    setIsDragging(false);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="border border-obsidian-800 bg-white p-6 shadow-brutal space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-obsidian-800 gap-3">
        <div>
          <span className="font-mono text-xs font-bold uppercase tracking-technical text-chalk-100 flex items-center gap-2">
            <Camera className="w-4 h-4 text-signal-red" />
            Karpo Lens: Multimodal Crop Disease Assistance
          </span>
          <p className="font-sans text-xs text-obsidian-300 mt-1 max-w-2xl leading-relaxed">
            Drag & drop or upload crop leaf photographs for automated pathology analysis via Z.ai Vision AI and authoritative ICAR symptom compendiums.
          </p>
        </div>

        {/* Crop Filter */}
        <div className="flex items-center gap-2 shrink-0">
          <label className="font-mono text-[11px] text-obsidian-400 uppercase">Crop:</label>
          <select
            value={selectedCrop}
            onChange={(e) => {
              setSelectedCrop(e.target.value);
              setInspectionResult(null);
            }}
            className="bg-obsidian-900 border border-obsidian-750 text-chalk-100 px-3 py-1 font-mono text-xs uppercase focus:outline-none focus:border-signal-red"
          >
            <option value="rice">Rice / भात</option>
            <option value="cotton">Cotton / कापूस</option>
            <option value="soybean">Soybean / सोयाबीन</option>
            <option value="wheat">Wheat / गहू</option>
            <option value="maize">Maize / मका</option>
          </select>
        </div>
      </div>

      {/* Upload & Preview Grid */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-start">
        {/* Upload & Drop Zone (Left Column) */}
        <div className="md:col-span-5 space-y-4">
          <input
            type="file"
            ref={fileInputRef}
            accept="image/jpeg,image/png,image/webp"
            onChange={handleFileChange}
            className="hidden"
          />

          {!previewUrl ? (
            <div
              onDragEnter={handleDragEnter}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed p-8 text-center cursor-pointer transition-all duration-200 select-none relative ${
                isDragging
                  ? "border-signal-red bg-obsidian-850 shadow-[0_0_20px_rgba(16,185,129,0.3)] scale-[1.01]"
                  : "border-obsidian-750 hover:border-signal-red bg-obsidian-900/60 hover:bg-obsidian-900"
              }`}
            >
              <div
                className={`w-14 h-14 rounded-full border flex items-center justify-center mx-auto mb-3 transition-transform ${
                  isDragging
                    ? "bg-signal-red/20 border-signal-red text-signal-lime scale-110 animate-bounce"
                    : "bg-obsidian-850 border-obsidian-750 text-signal-red"
                }`}
              >
                {isDragging ? <UploadCloud className="w-6 h-6" /> : <Upload className="w-6 h-6" />}
              </div>

              <div className="space-y-1">
                <span className="font-mono text-xs text-chalk-100 font-bold block uppercase tracking-technical">
                  {isDragging ? "Drop leaf photo now" : "Drag & Drop or Click to Upload"}
                </span>
                <span className="text-[11px] font-mono text-obsidian-400 block">
                  Leaf photograph (JPEG, PNG, WEBP &bull; Max 10 MB)
                </span>
                <span className="text-[10px] font-mono text-signal-red block pt-1">
                  Powered by Z.ai Multimodal Vision AI
                </span>
              </div>
            </div>
          ) : (
            <div
              onDragEnter={handleDragEnter}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              className={`border bg-obsidian-900 p-3 space-y-3 transition-all ${
                isDragging
                  ? "border-signal-red ring-2 ring-signal-red/40 bg-obsidian-850"
                  : "border-obsidian-750"
              }`}
            >
              <div className="relative aspect-video max-h-56 bg-black overflow-hidden flex items-center justify-center border border-obsidian-800">
                <img
                  src={previewUrl}
                  alt="Crop sample preview"
                  className="w-full h-full object-contain"
                />
                {isDragging && (
                  <div className="absolute inset-0 bg-obsidian-950/80 backdrop-blur-sm flex items-center justify-center">
                    <span className="font-mono text-xs font-bold text-signal-lime uppercase tracking-wider">
                      Drop to replace image
                    </span>
                  </div>
                )}
              </div>

              {selectedFile && (
                <div className="flex items-center justify-between font-mono text-[11px] text-obsidian-300 px-1">
                  <span className="truncate max-w-[200px]" title={selectedFile.name}>
                    {selectedFile.name}
                  </span>
                  <span>{(selectedFile.size / 1024).toFixed(0)} KB</span>
                </div>
              )}

              <div className="flex items-center gap-2 pt-1">
                <button
                  type="button"
                  onClick={handleUploadAndInspect}
                  disabled={loading}
                  className="flex-1 py-2.5 bg-signal-red hover:bg-signal-lime disabled:opacity-50 text-obsidian-950 font-mono text-xs uppercase font-black tracking-wider flex items-center justify-center gap-1.5 transition-colors shadow-[0_0_12px_rgba(16,185,129,0.25)]"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
                  <span>{loading ? "Inspecting with Z.ai..." : "Inspect Leaf with Z.ai"}</span>
                </button>

                <button
                  type="button"
                  onClick={handleReset}
                  className="px-3 py-2.5 bg-obsidian-850 hover:bg-obsidian-800 text-obsidian-300 border border-obsidian-750 font-mono text-xs uppercase"
                >
                  Reset
                </button>
              </div>

              <div className="text-[10px] font-mono text-obsidian-500 text-center">
                Tip: You can drag and drop another image here anytime to replace.
              </div>
            </div>
          )}

          {error && (
            <div className="p-3 bg-red-950/40 border border-red-500/40 text-red-400 text-xs font-mono flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* Diagnosis & ICAR Guidance Results (Right Column) */}
        <div className="md:col-span-7 space-y-4">
          {inspectionResult ? (
            <div className="space-y-4 font-mono text-xs">
              {/* Z.ai Verified Diagnosis Card */}
              {inspectionResult.status === "verified" && inspectionResult.diagnosis ? (
                <div className="p-4 bg-obsidian-900 border border-signal-red/60 space-y-3 shadow-brutal">
                  <div className="flex items-center justify-between border-b border-obsidian-800 pb-2">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full bg-signal-red animate-pulse" />
                      <span className="font-bold text-signal-lime text-xs uppercase tracking-technical flex items-center gap-1.5">
                        <CheckCircle className="w-4 h-4 text-signal-red" />
                        Z.ai Vision Diagnosis
                      </span>
                    </div>
                    {inspectionResult.confidence !== null && (
                      <span className="text-[10px] px-2 py-0.5 bg-signal-red text-obsidian-950 font-black border border-signal-red">
                        {(inspectionResult.confidence * 100).toFixed(0)}% Confidence
                      </span>
                    )}
                  </div>

                  {/* Primary Diagnosis Title */}
                  <div className="space-y-1">
                    <div className="text-[11px] text-obsidian-400 uppercase">Identified Condition:</div>
                    <div className="font-display font-black text-xl text-chalk-50 uppercase tracking-tight">
                      {inspectionResult.diagnosis}
                    </div>
                  </div>

                  {/* Visual Symptoms Observed */}
                  {inspectionResult.visual_symptoms && (
                    <div className="p-2.5 bg-[#F7F5EF] border border-obsidian-800 space-y-1">
                      <span className="text-[10px] text-signal-green uppercase tracking-wider font-bold block">
                        Visual Pathological Symptoms:
                      </span>
                      <p className="text-obsidian-200 font-sans text-xs leading-relaxed">
                        {inspectionResult.visual_symptoms}
                      </p>
                    </div>
                  )}

                  {/* Immediate Action Recommendation */}
                  {inspectionResult.treatment_recommendation && (
                    <div className="p-2.5 bg-[#F7F5EF] border border-obsidian-800 space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] text-signal-red uppercase tracking-wider font-bold block">
                          Recommended Agronomic Action:
                        </span>
                        {inspectionResult.urgency && (
                          <span
                            className={`text-[9px] px-1.5 py-0.2 border uppercase font-bold ${
                              inspectionResult.urgency === "High"
                                ? "bg-[#FDF2F2] border-[#B54747]/40 text-[#B54747]"
                                : inspectionResult.urgency === "Moderate"
                                ? "bg-[#FDF8F0] border-[#A66B18]/40 text-[#A66B18]"
                                : "bg-[#EAF0E6] border-[#357A4A]/40 text-[#357A4A]"
                            }`}
                          >
                            Urgency: {inspectionResult.urgency}
                          </span>
                        )}
                      </div>
                      <p className="text-chalk-200 font-sans text-xs leading-relaxed">
                        {inspectionResult.treatment_recommendation}
                      </p>
                    </div>
                  )}

                  <div className="flex flex-wrap gap-3 text-[10px] text-obsidian-400 pt-1 border-t border-obsidian-800/60">
                    <span>Provenance: {inspectionResult.data_provenance}</span>
                    <span className="ml-auto">
                      {inspectionResult.width}x{inspectionResult.height}px ({inspectionResult.format})
                    </span>
                  </div>
                </div>
              ) : inspectionResult.status === "quota_exceeded" ? (
                /* Honest Quota Exceeded Banner */
                <div className="p-4 bg-[#FDF8F0] border border-[#A66B18]/40 space-y-2.5 shadow-brutal">
                  <div className="flex items-center justify-between border-b border-obsidian-800 pb-2">
                    <span className="font-bold text-[#A66B18] flex items-center gap-1.5 text-xs uppercase tracking-technical">
                      <AlertTriangle className="w-4 h-4" />
                      Z.ai Vision Quota / Balance Recharge Needed
                    </span>
                    <span className="text-[10px] bg-white px-2 py-0.5 text-obsidian-300 border border-obsidian-700">
                      Code: 1113
                    </span>
                  </div>

                  <p className="text-chalk-200 font-sans text-xs leading-relaxed">
                    {inspectionResult.message}
                  </p>

                  <div className="p-2.5 bg-white border border-obsidian-800 text-[11px] font-mono text-obsidian-300 space-y-1">
                    <span className="text-[10px] text-[#A66B18] uppercase font-bold block">
                      Authentic Agricultural Data Principle:
                    </span>
                    <p className="font-sans text-[11px] text-obsidian-400 leading-snug">
                      To safeguard against incorrect pesticide and chemical application, Karpo strictly avoids fabricating synthetic diagnoses when external vision quotas are exhausted.
                    </p>
                  </div>

                  <div className="flex flex-wrap gap-3 text-[10px] text-obsidian-400 pt-1 border-t border-obsidian-800/60">
                    <span>Image: {inspectionResult.width}x{inspectionResult.height}px</span>
                    <span>Format: {inspectionResult.format}</span>
                    <span>Size: {(inspectionResult.size_bytes / 1024).toFixed(1)} KB</span>
                    <span className="text-signal-lime font-bold ml-auto flex items-center gap-1">
                      <CheckCircle className="w-3 h-3 text-signal-red" /> Leaf Image Validated
                    </span>
                  </div>
                </div>
              ) : (
                /* Fallback Honest Offline State */
                <div className="p-4 bg-obsidian-900 border border-obsidian-750 space-y-2">
                  <div className="flex items-center justify-between border-b border-obsidian-800 pb-2">
                    <span className="font-bold text-obsidian-300 flex items-center gap-1.5 text-xs">
                      <ShieldAlert className="w-4 h-4 text-obsidian-400" />
                      Vision Model Status
                    </span>
                    <span className="text-[10px] bg-obsidian-800 px-2 py-0.5 text-obsidian-300 border border-obsidian-700">
                      Category: {inspectionResult.data_category}
                    </span>
                  </div>

                  <p className="text-obsidian-300 font-sans text-xs leading-relaxed">
                    {inspectionResult.message}
                  </p>

                  <div className="flex flex-wrap gap-3 text-[10px] text-obsidian-400 pt-1 border-t border-obsidian-800/60">
                    <span>Image: {inspectionResult.width}x{inspectionResult.height}px</span>
                    <span>Format: {inspectionResult.format}</span>
                    <span>Size: {(inspectionResult.size_bytes / 1024).toFixed(1)} KB</span>
                    <span className="text-signal-lime font-bold ml-auto flex items-center gap-1">
                      <CheckCircle className="w-3 h-3 text-signal-red" /> Validated
                    </span>
                  </div>
                </div>
              )}

              {/* Authoritative ICAR Disease Compendium Reference */}
              <div className="space-y-2">
                <div className="flex items-center justify-between text-xs font-bold text-chalk-100 uppercase pb-1 border-b border-obsidian-800">
                  <span className="flex items-center gap-1.5">
                    <FileText className="w-3.5 h-3.5 text-signal-red" />
                    Authoritative ICAR Diagnostic Symptoms ({inspectionResult.crop_evaluated?.toUpperCase() || selectedCrop.toUpperCase()})
                  </span>
                  <span className="text-[10px] text-obsidian-400 font-normal">Official Guidelines</span>
                </div>

                <div className="space-y-3">
                  {inspectionResult.icar_symptom_guide.map((item, idx) => (
                    <div key={idx} className="p-3.5 bg-obsidian-900 border border-obsidian-800 space-y-1.5">
                      <div className="font-bold text-chalk-100 text-xs flex items-center justify-between">
                        <span>{item.disease_name}</span>
                      </div>
                      <p className="text-obsidian-300 font-sans text-xs">
                        <strong>Visual Symptoms:</strong> {item.key_symptoms}
                      </p>
                      <p className="text-signal-lime/90 font-sans text-[11px]">
                        <strong>Cultural Control:</strong> {item.cultural_management}
                      </p>
                      <div className="text-[10px] text-obsidian-500 pt-1 border-t border-obsidian-800/60">
                        Reference: {item.source}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="border border-dashed border-obsidian-800 bg-obsidian-900/40 p-8 text-center space-y-2">
              <Info className="w-6 h-6 text-obsidian-500 mx-auto" />
              <h4 className="font-mono text-xs uppercase font-bold text-chalk-200">
                Awaiting Crop Leaf Sample
              </h4>
              <p className="font-sans text-xs text-obsidian-400 max-w-md mx-auto">
                Drag and drop or upload a photograph of crop leaves exhibiting spots, blight, or curling. Karpo Lens will validate the image and analyze symptoms using Z.ai Multimodal Vision AI alongside official ICAR diagnostic symptom guides.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

