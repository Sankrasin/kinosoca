import { useState, useEffect } from "react";
import MovieRow from "../components/movie/MovieRow";
import SearchBar from "../components/search/SearchBar";
import Loader from "../components/common/Loader";
import { movieApi } from "../api/movieApi";
import { searchApi } from "../api/searchApi";

export default function HomePage() {
  const [trending, setTrending] = useState([]);
  const [popular, setPopular] = useState([]);
  const [topRated, setTopRated] = useState([]);
  const [loading, setLoading] = useState(true);

  // local search state
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    loadMovies();
  }, []);

  const loadMovies = async () => {
    try {
      setLoading(true);
      const [trendingRes, popularRes, topRatedRes] = await Promise.all([
        movieApi.getTrending(1, 6),
        movieApi.getPopular(1, 6),
        movieApi.getTopRated(1, 6),
      ]);
      setTrending(trendingRes.data.items || []);
      setPopular(popularRes.data.items || []);
      setTopRated(topRatedRes.data.items || []);
    } catch (error) {
      console.error("Failed to load movies:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (query) => {
    if (!query) return;
    try {
      setIsSearching(true);
      setSearchQuery(query);
      const response = await searchApi.search({
        query,
        page: 1,
        page_size: 20,
      });
      setSearchResults(response.data.items || []);
    } catch (error) {
      console.error("Search failed:", error);
    } finally {
      setIsSearching(false);
    }
  };

  const clearSearch = () => {
    setSearchResults([]);
    setSearchQuery("");
  };

  if (loading && !trending.length) {
    return <Loader />;
  }

  const heroMovie = trending.length > 0 ? trending[0] : null;

  return (
    <div className="space-y-12 pb-12">
      <div className="relative w-full h-[600px] -mt-24 mb-12 rounded-3xl overflow-hidden shadow-2xl">
        <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none">
          {heroMovie?.backdrop_path ? (
            <img
              src={`https://image.tmdb.org/t/p/original${heroMovie.backdrop_path}`}
              alt="Hero Backdrop"
              className="w-full h-full object-cover opacity-30 object-top"
            />
          ) : null}
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary/50 to-primary"></div>
          <div className="absolute inset-0 bg-gradient-to-t from-primary via-primary/80 to-transparent"></div>
          <div className="absolute top-20 left-10 w-96 h-96 bg-cyan-500/20 rounded-full blur-[120px]" />
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-500/20 rounded-full blur-[120px]" />
        </div>

        <div className="absolute inset-0 flex flex-col justify-center px-12 lg:px-24">
          <div className="max-w-3xl animate-fade-in">
            <h1 className="text-5xl md:text-7xl font-heading font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-300 drop-shadow-2xl tracking-tighter leading-tight mb-6">
              Unlock Your Next{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent to-blue-500">
                Binge
              </span>
            </h1>

            <p className="text-xl text-gray-300 mb-10 max-w-2xl leading-relaxed font-medium">
              Over the scroll? Describe your vibe. We'll find it.
            </p>

            <div className="glass p-3 rounded-2xl max-w-4xl shadow-2xl w-full">
              <SearchBar
                onSearch={handleSearch}
                placeholder="Search movies by title..."
              />
            </div>
          </div>
        </div>
      </div>

      {isSearching ? (
        <Loader />
      ) : searchResults.length > 0 ? (
        <div className="animate-fade-in">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold text-gray-100">
              Search Results for "{searchQuery}"
            </h2>
            <button
              onClick={clearSearch}
              className="btn-secondary text-sm px-4 py-2"
            >
              Clear Results
            </button>
          </div>
          <MovieRow title="" movies={searchResults} />
        </div>
      ) : (
        <>
          <MovieRow title="Trending Now" movies={trending} />
          <MovieRow title="Popular" movies={popular} />
          <MovieRow title="Top Rated" movies={topRated} />
        </>
      )}
    </div>
  );
}
