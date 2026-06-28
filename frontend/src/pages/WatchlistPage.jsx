import { useState, useEffect } from "react";
import { Trash2, Eye } from "lucide-react";
import MovieGrid from "../components/movie/MovieGrid";
import Loader from "../components/common/Loader";
import { watchlistApi } from "../api/watchlistApi";

export default function WatchlistPage() {
  const [watchlist, setWatchlist] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    loadWatchlist();
  }, []);

  const loadWatchlist = async () => {
    try {
      setLoading(true);
      const response = await watchlistApi.getWatchlist();
      setWatchlist(response.data.items || []);
    } catch (error) {
      console.error("Failed to load watchlist:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleRemove = async (movieId) => {
    try {
      await watchlistApi.removeFromWatchlist(movieId);
      setWatchlist(watchlist.filter((item) => item.movie_id !== movieId));
    } catch (error) {
      console.error("Failed to remove from watchlist:", error);
    }
  };

  const handleMarkWatched = async (movieId) => {
    try {
      await watchlistApi.updateWatchlistStatus(movieId, "watched");
      setWatchlist(
        watchlist.map((item) =>
          item.movie_id === movieId ? { ...item, status: "watched" } : item,
        ),
      );
    } catch (error) {
      console.error("Failed to mark as watched:", error);
    }
  };

  const filteredWatchlist =
    filter === "all"
      ? watchlist
      : watchlist.filter((item) => item.status === filter);

  const movies = filteredWatchlist.map((item) => item.movie);

  if (loading) {
    return <Loader />;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-gray-100 mb-2">My Watchlist</h1>
        <p className="text-gray-400">
          {watchlist.length} movie{watchlist.length !== 1 ? "s" : ""} in your
          watchlist
        </p>
      </div>

      {watchlist.length > 0 && (
        <div className="flex gap-2">
          <button
            onClick={() => setFilter("all")}
            className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
              filter === "all"
                ? "bg-accent text-white"
                : "bg-secondary text-gray-100 hover:bg-gray-600"
            }`}
          >
            All ({watchlist.length})
          </button>
          <button
            onClick={() => setFilter("saved")}
            className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
              filter === "saved"
                ? "bg-accent text-white"
                : "bg-secondary text-gray-100 hover:bg-gray-600"
            }`}
          >
            To Watch ({watchlist.filter((i) => i.status === "saved").length})
          </button>
          <button
            onClick={() => setFilter("watched")}
            className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
              filter === "watched"
                ? "bg-accent text-white"
                : "bg-secondary text-gray-100 hover:bg-gray-600"
            }`}
          >
            Watched ({watchlist.filter((i) => i.status === "watched").length})
          </button>
        </div>
      )}

      {filteredWatchlist.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-400 text-lg">
            {watchlist.length === 0
              ? "Your watchlist is empty. Start adding movies!"
              : "No movies in this category."}
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          <MovieGrid movies={movies} />
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {filteredWatchlist.map((item) => (
              <div key={item.id} className="flex gap-2">
                {item.status === "saved" && (
                  <button
                    onClick={() => handleMarkWatched(item.movie_id)}
                    className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-secondary hover:bg-gray-600 rounded transition-colors text-sm"
                  >
                    <Eye size={16} />
                    Mark Watched
                  </button>
                )}
                <button
                  onClick={() => handleRemove(item.movie_id)}
                  className="flex items-center justify-center gap-2 px-3 py-2 bg-red-600 hover:bg-red-700 rounded transition-colors text-sm"
                >
                  <Trash2 size={16} />
                  Remove
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
