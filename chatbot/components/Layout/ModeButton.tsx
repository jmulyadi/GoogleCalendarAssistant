import { useEffect, useState } from "react";
export default function ThemeToggle() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    const darkMode = localStorage.getItem("theme") === "dark";
    setIsDarkMode(darkMode);
  }, []);

  const toggleTheme = () => {
    const newTheme = isDarkMode ? "light" : "dark";
    localStorage.setItem("theme", newTheme);
    document.documentElement.classList.toggle("dark", newTheme === "dark");
    setIsDarkMode(!isDarkMode);
  };

  return (
    <button
      onClick={toggleTheme}
      aria-label="Toggle theme"
      className="w-5 h-7 p-0"
    >
      {isDarkMode ? (
        <img
          src="/sun-fog-svgrepo-com2.svg"
          alt="sun"
          className="w-full h-full origin-center scale-150"
        />
      ) : (
        <img
          src="moon-svgrepo-com.svg"
          alt="sun"
          className="w-full h-full origin-center scale-150"
        />
      )}
    </button>
  );
}
