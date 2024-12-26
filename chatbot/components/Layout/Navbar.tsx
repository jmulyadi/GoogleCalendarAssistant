import { FC } from "react";
import DarkModeToggle from "./ModeButton";

export const Navbar: FC = () => {
  return (
    <div className="flex h-[50px] sm:h-[60px] border-b border-neutral-300 py-2 px-2 sm:px-8 items-center justify-between">
      <div className="font-bold text-3xl flex items-center">
        <a
          className="ml-2 hover:opacity-50"
          href="https://joshmulyadi.netlify.app/"
        >
          Google Calendar Assistant
        </a>
      </div>
      <div className="text-sm sm:text-base text-neutral-900 font-semibold rounded-lg px-4 py-2 bg-neutral-200 hover:bg-neutral-300 focus:outline-none focus:ring-1 focus:ring-neutral-300 dark:text-textPrimary dark:bg-buttonPrimary dark:hover:bg-buttonHover">
        <DarkModeToggle />
      </div>
    </div>
  );
};
