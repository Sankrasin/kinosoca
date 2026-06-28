import { useState } from "react";
import { ChevronDown } from "lucide-react";

export default function FilterPanel({ onFilterChange, providers = [] }) {
  const [expanded, setExpanded] = useState(false);
  const [filters, setFilters] = useState({
    genre: "",
    actor: "",
    country: "",
    language: "",
    year: "",
    minRating: "",
    provider: "",
  });

  const handleChange = (key, value) => {
    setFilters({ ...filters, [key]: value });
  };

  const handleApply = () => {
    onFilterChange(filters);
  };

  const handleClear = () => {
    const emptyFilters = {
      genre: "",
      actor: "",
      country: "",
      language: "",
      year: "",
      minRating: "",
      provider: "",
    };
    setFilters(emptyFilters);
    onFilterChange(emptyFilters);
  };

  return (
    <div className="glass p-5 rounded-2xl mb-8 shadow-lg border border-white/10 relative overflow-hidden group transition-all duration-300">
      <div className="absolute top-0 right-0 w-64 h-64 bg-accent/5 rounded-full blur-3xl -mr-32 -mt-32 transition-colors group-hover:bg-accent/10" />

      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between font-heading font-bold text-lg text-white hover:text-accent transition-colors relative z-10"
      >
        <span className="flex items-center gap-2">
          <span className="w-1 h-5 bg-accent rounded-full inline-block"></span>
          Advanced Filters
        </span>
        <ChevronDown
          size={22}
          className={`transition-transform duration-300 text-gray-400 ${expanded ? "rotate-180 text-accent" : ""}`}
        />
      </button>

      {expanded && (
        <div className="mt-6 relative z-10 animate-slide-up">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <label className="block text-xs font-bold tracking-wider uppercase text-gray-400 mb-2 ml-1">
                Genre
              </label>
              <select
                value={filters.genre}
                onChange={(e) => handleChange("genre", e.target.value)}
                className="w-full px-4 py-3 bg-secondary border border-white/10 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent/50 transition-all duration-300 shadow-inner appearance-none"
              >
                <option value="">Any Genre</option>
                <option value="Action">Action</option>
                <option value="Adventure">Adventure</option>
                <option value="Animation">Animation</option>
                <option value="Comedy">Comedy</option>
                <option value="Crime">Crime</option>
                <option value="Documentary">Documentary</option>
                <option value="Drama">Drama</option>
                <option value="Family">Family</option>
                <option value="Fantasy">Fantasy</option>
                <option value="History">History</option>
                <option value="Horror">Horror</option>
                <option value="Music">Music</option>
                <option value="Mystery">Mystery</option>
                <option value="Romance">Romance</option>
                <option value="Science Fiction">Science Fiction</option>
                <option value="Thriller">Thriller</option>
                <option value="War">War</option>
                <option value="Western">Western</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold tracking-wider uppercase text-gray-400 mb-2 ml-1">
                Actor / Actress
              </label>
              <select
                value={filters.actor}
                onChange={(e) => handleChange("actor", e.target.value)}
                className="w-full px-4 py-3 bg-secondary border border-white/10 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent/50 transition-all duration-300 shadow-inner appearance-none"
              >
                <option value="">Any Actor</option>
                <option value="Tom Cruise">Tom Cruise</option>
                <option value="Leonardo DiCaprio">Leonardo DiCaprio</option>
                <option value="Brad Pitt">Brad Pitt</option>
                <option value="Scarlett Johansson">Scarlett Johansson</option>
                <option value="Robert Downey Jr.">Robert Downey Jr.</option>
                <option value="Tom Hanks">Tom Hanks</option>
                <option value="Denzel Washington">Denzel Washington</option>
                <option value="Meryl Streep">Meryl Streep</option>
                <option value="Christian Bale">Christian Bale</option>
                <option value="Margot Robbie">Margot Robbie</option>
                <option value="Ryan Gosling">Ryan Gosling</option>
                <option value="Emma Stone">Emma Stone</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold tracking-wider uppercase text-gray-400 mb-2 ml-1">
                Country
              </label>
              <select
                value={filters.country}
                onChange={(e) => handleChange("country", e.target.value)}
                className="w-full px-4 py-3 bg-secondary border border-white/10 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent/50 transition-all duration-300 shadow-inner appearance-none"
              >
                <option value="">Any Country</option>
                <option value="US">United States</option>
                <option value="IN">India</option>
                <option value="KR">South Korea</option>
                <option value="JP">Japan</option>
                <option value="GB">United Kingdom</option>
                <option value="FR">France</option>
                <option value="DE">Germany</option>
                <option value="IT">Italy</option>
                <option value="ES">Spain</option>
                <option value="CA">Canada</option>
                <option value="AU">Australia</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold tracking-wider uppercase text-gray-400 mb-2 ml-1">
                Language
              </label>
              <select
                value={filters.language}
                onChange={(e) => handleChange("language", e.target.value)}
                className="w-full px-4 py-3 bg-secondary border border-white/10 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent/50 transition-all duration-300 shadow-inner appearance-none"
              >
                <option value="">Any Language</option>
                <option value="en">English</option>
                <option value="ko">Korean</option>
                <option value="ja">Japanese</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="hi">Hindi</option>
                <option value="te">Telugu</option>
                <option value="ta">Tamil</option>
                <option value="de">German</option>
                <option value="it">Italian</option>
                <option value="zh">Chinese</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold tracking-wider uppercase text-gray-400 mb-2 ml-1">
                Release Year
              </label>
              <select
                value={filters.year}
                onChange={(e) => handleChange("year", e.target.value)}
                className="w-full px-4 py-3 bg-secondary border border-white/10 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent/50 transition-all duration-300 shadow-inner appearance-none"
              >
                <option value="">Any Year</option>
                {[...Array(30)].map((_, i) => {
                  const year = new Date().getFullYear() - i;
                  return (
                    <option key={year} value={year}>
                      {year}
                    </option>
                  );
                })}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold tracking-wider uppercase text-gray-400 mb-2 ml-1">
                Min Rating
              </label>
              <select
                value={filters.minRating}
                onChange={(e) => handleChange("minRating", e.target.value)}
                className="w-full px-4 py-3 bg-secondary border border-white/10 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent/50 transition-all duration-300 shadow-inner appearance-none"
              >
                <option value="">Any Rating</option>
                <option value="9.0">9.0+ (Masterpiece)</option>
                <option value="8.0">8.0+ (Excellent)</option>
                <option value="7.5">7.5+ (Very Good)</option>
                <option value="7.0">7.0+ (Good)</option>
                <option value="6.0">6.0+ (Average)</option>
                <option value="5.0">5.0+ (Mixed)</option>
              </select>
            </div>

            {providers.length > 0 && (
              <div>
                <label className="block text-xs font-bold tracking-wider uppercase text-gray-400 mb-2 ml-1">
                  Provider
                </label>
                <select
                  value={filters.provider}
                  onChange={(e) => handleChange("provider", e.target.value)}
                  className="w-full px-4 py-3 bg-secondary border border-white/10 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent/50 transition-all duration-300 shadow-inner appearance-none"
                >
                  <option value="">Any Provider</option>
                  {providers.map((p) => (
                    <option key={p.provider_id} value={p.name}>
                      {p.name}
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>

          <div className="flex gap-4 mt-8 pt-6 border-t border-white/10 justify-end">
            <button onClick={handleClear} className="btn-secondary h-12">
              Clear
            </button>
            <button onClick={handleApply} className="btn-primary h-12">
              Apply Filters
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
