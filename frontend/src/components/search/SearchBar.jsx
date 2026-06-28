import { useState } from "react";
import { Search } from "lucide-react";

export default function SearchBar({
  onSearch,
  placeholder = "Search movies...",
  buttonText = "Search",
  type = "text",
}) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="relative flex gap-3 items-center">
        <div className="flex-1 relative group">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={placeholder}
            className={`w-full px-6 py-4 bg-white/5 border border-white/10 text-white rounded-2xl focus:outline-none focus:ring-2 focus:ring-${type === "ai" ? "accent" : "blue-500"}/50 focus:border-${type === "ai" ? "accent" : "blue-500"}/50 placeholder-gray-400 transition-all duration-300 shadow-inner`}
          />
          <Search
            className={`absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 transition-colors duration-300 group-focus-within:text-${type === "ai" ? "accent" : "blue-500"}`}
            size={22}
          />
        </div>

        <button
          type="submit"
          className={`px-8 h-[56px] text-lg rounded-xl font-bold tracking-wide transition-all duration-300 shadow-lg hover:-translate-y-0.5 text-white ${
            type === "ai"
              ? "bg-gradient-to-r from-accent to-purple-600 shadow-neon-purple/40 hover:shadow-neon-purple"
              : "bg-gradient-to-r from-blue-600 to-cyan-500 shadow-neon-cyan/40 hover:shadow-neon-cyan"
          }`}
        >
          {buttonText}
        </button>
      </div>
    </form>
  );
}
