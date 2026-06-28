import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import MovieGrid from "../components/movie/MovieGrid";
import FilterPanel from "../components/search/FilterPanel";
import Pagination from "../components/common/Pagination";
import Loader from "../components/common/Loader";
import SearchBar from "../components/search/SearchBar";
import { searchApi } from "../api/searchApi";
import { providerApi } from "../api/providerApi";

export default function SearchPage() {
  const [searchParams] = useSearchParams();
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [filters, setFilters] = useState({});
  const [providers, setProviders] = useState([]);

  // search state for ai
  const [isAiMode, setIsAiMode] = useState(false);
  const [aiQuery, setAiQuery] = useState("");

  const initialQuery = searchParams.get("query") || "";

  useEffect(() => {
    loadProviders();
  }, []);

  useEffect(() => {
    if (!isAiMode) {
      performSearch();
    }
  }, [initialQuery, page, filters, isAiMode]);

  const loadProviders = async () => {
    try {
      const response = await providerApi.getProviders("IN");
      setProviders(response.data || []);
    } catch (error) {
      console.error("Failed to load providers:", error);
    }
  };

  const performSearch = async () => {
    try {
      setLoading(true);

      const cleanedFilters = Object.fromEntries(
        Object.entries(filters).filter(([_, v]) => v !== ""),
      );

      const searchParams = {
        query: initialQuery,
        page,
        page_size: 20,
        ...cleanedFilters,
      };
      const response = await searchApi.search(searchParams);
      setResults(response.data.items || []);
      setTotalPages(response.data.total_pages || 1);
    } catch (error) {
      console.error("Search failed:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleAiSearch = async (query) => {
    if (!query) return;
    try {
      setLoading(true);
      setIsAiMode(true);
      setAiQuery(query);
      const response = await searchApi.semanticSearch(query, 20);
      setResults(response.data || []);
      setTotalPages(1); // ai gives a flat list
    } catch (error) {
      console.error("Semantic search failed:", error);
    } finally {
      setLoading(false);
    }
  };

  const clearAiSearch = () => {
    setIsAiMode(false);
    setAiQuery("");
    setPage(1);
  };

  const handleFilterChange = (newFilters) => {
    setIsAiMode(false); // back to normal search if filter changes
    setFilters(newFilters);
    setPage(1);
  };

  const handlePageChange = (newPage) => {
    setPage(newPage);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div className="space-y-8">
      <div className="glass-card p-8 bg-gradient-to-br from-secondary to-primary border-accent/20 border relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-accent/10 rounded-full blur-[100px] pointer-events-none" />
        <h2 className="text-2xl font-heading font-bold text-transparent bg-clip-text bg-gradient-to-r from-accent to-blue-400 mb-4 tracking-wide">
          AI Semantic Search
        </h2>
        <p className="text-gray-400 mb-6">
          Describe the exact vibe you're looking for, and our AI will find it.
          (e.g., "A dark detective story with a plot twist")
        </p>
        <SearchBar
          onSearch={handleAiSearch}
          placeholder="Describe your vibe..."
          buttonText="AI Search"
          type="ai"
        />
      </div>

      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-100 mb-2">
            {isAiMode
              ? `AI Results for "${aiQuery}"`
              : `Search Results for "${initialQuery}"`}
          </h1>
          <p className="text-gray-400">
            Found {results.length > 0 ? "movies" : "no movies"} matching your{" "}
            {isAiMode ? "vibe" : "search"}
          </p>
        </div>
        {isAiMode && (
          <button
            onClick={clearAiSearch}
            className="btn-secondary text-sm px-4 py-2"
          >
            Clear AI Search
          </button>
        )}
      </div>

      {!isAiMode && (
        <FilterPanel
          onFilterChange={handleFilterChange}
          providers={providers}
        />
      )}

      {loading ? (
        <Loader />
      ) : (
        <>
          <MovieGrid movies={results} />
          {!isAiMode && totalPages > 1 && (
            <Pagination
              page={page}
              totalPages={totalPages}
              onPageChange={handlePageChange}
            />
          )}
        </>
      )}
    </div>
  );
}
