import React from "react";
import { RotateCcw } from "lucide-react";
import { useLanguage } from "../context/LanguageContext";

interface RestartButtonProps {
  onRestart: () => void;
  className?: string;
}

export const RestartButton: React.FC<RestartButtonProps> = ({
  onRestart,
  className = "",
}) => {
  const { t } = useLanguage();

  return (
    <button
      onClick={onRestart}
      className={`flex items-center gap-2 px-3 py-1.5 text-sm font-medium 
                 text-gray-600 hover:text-blue-600 hover:bg-blue-50 
                 rounded-md transition-colors ${className}`}
      aria-label={t("restart")}
    >
      <RotateCcw className="w-4 h-4" />
      <span className="hidden sm:block">{t("restart")}</span>
    </button>
  );
};
