import React from "react";
import logo from "../assets/logo.svg";
import { LanguageToggle } from "./LanguageToggle";
import { RestartButton } from "./RestartButton";

interface HeaderProps {
  onRestart: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onRestart }) => {
  return (
    <div className="bg-white border-b border-gray-200 p-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <img src={logo} alt="InnAlyze Logo" className="w-8 h-8" />
          <h1 className="text-xl font-semibold bg-gradient-to-r from-emerald-500 to-purple-600 bg-clip-text text-transparent">
            InnAlyze Agent
          </h1>
        </div>
        <div className="flex items-center gap-2">
          <RestartButton onRestart={onRestart} />
          <LanguageToggle />
        </div>
      </div>
    </div>
  );
};
