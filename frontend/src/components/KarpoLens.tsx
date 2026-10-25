import React, { useState, useRef } from "react";
import { Camera, Upload, AlertCircle, ShieldAlert, CheckCircle, FileText, RefreshCw, Info } from "lucide-react";
import { api } from "../api/client";
import { LensInspectionResponse } from "../types/api";

export const KarpoLens: React.FC = () => {
  const [selectedCrop, setSelectedCrop] = useState<string>("rice");
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [inspectionResult, setInspectionResult] = useState<LensInspectionResponse | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      setError("Please select a valid image file (JPEG, PNG, or WEBP).");
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

  const handleUploadAndInspect = async () => {
    if (!selectedFile) {
      setError("Please select or capture a photo first.");
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
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="border border-obsidian-750 bg-obsidian-950 p-6 shadow-brutal space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-obsidian-800 gap-3">
        <div>
          <span className="font-mono text-xs font-bold uppercase tracking-technical text-chalk-100 flex items-center gap-2">
            <Camera className="w-4 h-4 text-signal-red" />
            Karpo Lens: Crop Disease Assistance
          </span>
          <p className="font-sans text-xs text-obsidian-300 mt-1 max-w-2xl leading-relaxed">
            Upload or capture leaf photos for field symptom validation. Backed by verified ICAR plant pathology protocols with zero fabricated diagnoses.
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
        {/* Upload Zone (Left Column) */}
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
              onClick={() => fileInputRef.current?.click()}
              className="border-2 border-dashed border-obsidian-750 hover:border-signal-red bg-obsidian-900/60 p-8 text-center cursor-pointer transition-colors space-y-3"
            >
              <div className="w-12 h-12 rounded-full bg-obsidian-850 border border-obsidian-750 flex items-center justify-center mx-auto text-signal-red">
                <Upload className="w-5 h-5" />
              </div>
              <div className="space-y-1">
                <span className="font-mono text-xs text-chalk-200 font-bold block">
                  Click to Upload or Capture Leaf Photo
                </span>
                <span className="text-[11px] font-mono text-obsidian-400 block">
                  JPEG, PNG, WEBP (Max 10 MB)
                </span>
              </div>
            </div>
          ) : (
            <div className="border border-obsidian-750 bg-obsidian-900 p-3 space-y-3">
              <div className="relative aspect-video max-h-56 bg-black overflow-hidden flex items-center justify-center">
                <img
                  src={previewUrl}
                  alt="Crop sample preview"
                  className="w-full h-full object-contain"
                />
              </div>

              {selectedFile && (
                <div className="flex items-center justify-between font-mono text-[11px] text-obsidian-300 px-1">
                  <span className="truncate max-w-[200px]">{selectedFile.name}</span>
                  <span>{(selectedFile.size / 1024).toFixed(0)} KB</span>
                </div>
              )}

              <div className="flex items-center gap-2 pt-1">
                <button
                  type="button"
                  onClick={handleUploadAndInspect}
                  disabled={loading}
                  className="flex-1 py-2 bg-signal-red hover:bg-red-600 disabled:opacity-50 text-white font-mono text-xs uppercase font-bold tracking-wider flex items-center justify-center gap-1.5 transition-colors"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
                  <span>{loading ? "Inspecting Image..." : "Inspect Leaf Photo"}</span>
                </button>

                <button
                  type="button"
                  onClick={handleReset}
                  className="px-3 py-2 bg-obsidian-850 hover:bg-obsidian-800 text-obsidian-300 border border-obsidian-750 font-mono text-xs uppercase"
                >
                  Reset
                </button>
              </div>
            </div>
          )}

          {error && (
            <div className="p-3 bg-signal-red/10 border border-signal-red/30 text-signal-red text-xs font-mono flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* Diagnosis & ICAR Guidance Results (Right Column) */}
        <div className="md:col-span-7 space-y-4">
          {inspectionResult ? (
            <div className="space-y-4 font-mono text-xs">
              {/* Honest Model Status Banner */}
              <div className="p-4 bg-obsidian-900 border border-amber-500/40 space-y-2">
                <div className="flex items-center justify-between border-b border-obsidian-800 pb-2">
                  <span className="font-bold text-amber-400 flex items-center gap-1.5 text-xs">
                    <ShieldAlert className="w-4 h-4" />
                    Automated Diagnosis Model Offline
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
                  <span className="text-emerald-400 font-bold ml-auto flex items-center gap-1">
                    <CheckCircle className="w-3 h-3" /> Image Validated
                  </span>
                </div>
              </div>

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
                      <p className="text-emerald-400/90 font-sans text-[11px]">
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
                Upload a photograph of crop leaves exhibiting spots, blight, or curling. Karpo validates the image structure and provides official ICAR diagnostic symptom guides for comparison.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
