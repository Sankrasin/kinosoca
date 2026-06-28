import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Bookmark, BookmarkCheck, ArrowLeft, Star } from "lucide-react";
import MovieRow from "../components/movie/MovieRow";
import ProviderBadge from "../components/movie/ProviderBadge";
import RecommendationExplanation from "../components/movie/RecommendationExplanation";
import Loader from "../components/common/Loader";
import { useAuth } from "../hooks/useAuth";
import { movieApi } from "../api/movieApi";
import { recommendationApi } from "../api/recommendationApi";
import { watchlistApi } from "../api/watchlistApi";

export default function MovieDetailsPage() {
  const { movieId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [movie, setMovie] = useState(null);
  const [similar, setSimilar] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isInWatchlist, setIsInWatchlist] = useState(false);
  const [savingWatchlist, setSavingWatchlist] = useState(false);

  useEffect(() => {
    loadMovieData();
  }, [movieId]);

  const loadMovieData = async () => {
    try {
      setLoading(true);
      const [movieRes, similarRes] = await Promise.all([
        movieApi.getMovieDetail(movieId),
        recommendationApi.getSimilar(movieId, 8),
      ]);
      setMovie(movieRes.data);
      setSimilar(similarRes.data.items || []);

      if (user) {
        checkWatchlistStatus();
      }
    } catch (error) {
      console.error("Failed to load movie data:", error);
    } finally {
      setLoading(false);
    }
  };

  const checkWatchlistStatus = async () => {
    try {
      const response = await watchlistApi.getWatchlist();
      const inWatchlist = response.data.items.some(
        (item) => item.movie_id === parseInt(movieId),
      );
      setIsInWatchlist(inWatchlist);
    } catch (error) {
      console.error("Failed to check watchlist status:", error);
    }
  };

  const handleWatchlistToggle = async () => {
    if (!user) {
      navigate("/login");
      return;
    }

    try {
      setSavingWatchlist(true);
      if (isInWatchlist) {
        await watchlistApi.removeFromWatchlist(movieId);
        setIsInWatchlist(false);
      } else {
        await watchlistApi.addToWatchlist(movieId);
        setIsInWatchlist(true);
      }
    } catch (error) {
      console.error("Failed to toggle watchlist:", error);
    } finally {
      setSavingWatchlist(false);
    }
  };

  if (loading || !movie) {
    return <Loader />;
  }

  const backdropUrl = movie.backdrop_path
    ? `https://image.tmdb.org/t/p/w1280${movie.backdrop_path}`
    : null;

  return (
    <div className="space-y-12 pb-12 -mt-24">
      <div className="relative w-full h-[70vh] min-h-[500px]">
        {backdropUrl ? (
          <img
            src={backdropUrl}
            alt={movie.title}
            className="absolute inset-0 w-full h-full object-cover object-top opacity-60"
          />
        ) : (
          <div className="absolute inset-0 bg-gradient-to-br from-secondary to-primary" />
        )}

        <div className="absolute inset-0 bg-gradient-to-t from-primary via-primary/80 to-transparent" />
        <div className="absolute inset-0 bg-gradient-to-r from-primary via-primary/40 to-transparent" />

        <button
          onClick={() => navigate(-1)}
          className="absolute top-24 left-6 md:left-12 flex items-center gap-2 text-white/70 hover:text-white transition-colors z-40 glass px-4 py-2 rounded-full font-bold shadow-neon-purple"
        >
          <ArrowLeft size={18} />
          Back
        </button>

        <div className="absolute inset-0 flex flex-col justify-end px-6 md:px-12 pb-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12 items-end">
            <div className="hidden md:block md:col-span-1 transform translate-y-24 z-20">
              <div className="glass-card p-2 rounded-3xl">
                <img
                  src={
                    movie.poster_path
                      ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
                      : "https://via.placeholder.com/300x450?text=No+Image"
                  }
                  alt={movie.title}
                  className="w-full rounded-2xl shadow-2xl"
                />
              </div>
            </div>

            <div className="md:col-span-3 z-20 animate-fade-in">
              <h1 className="text-5xl md:text-7xl font-heading font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-300 drop-shadow-2xl tracking-tighter mb-2">
                {movie.title}
              </h1>
              {movie.original_title && movie.original_title !== movie.title && (
                <p className="text-xl text-gray-400 font-medium tracking-wide mb-4">
                  {movie.original_title}
                </p>
              )}

              <div className="flex items-center gap-3 flex-wrap mb-6">
                <span className="badge border-accent/30 text-white">
                  {movie.release_year || "N/A"}
                </span>
                <span className="badge border-accent/30 text-white">
                  {movie.runtime ? `${movie.runtime} min` : "N/A"}
                </span>
                <span className="badge border-accent/30 text-accent flex items-center gap-1 shadow-[0_0_10px_rgba(168,85,247,0.4)]">
                  <Star size={14} className="fill-accent" />{" "}
                  {movie.vote_average.toFixed(1)}{" "}
                  <span className="text-gray-400 font-normal ml-1">
                    ({movie.vote_count} votes)
                  </span>
                </span>
              </div>

              <div className="flex items-center gap-4">
                <button
                  onClick={handleWatchlistToggle}
                  disabled={savingWatchlist}
                  className={`flex items-center gap-2 px-8 py-4 rounded-xl font-bold tracking-wide transition-all duration-300 shadow-lg ${
                    isInWatchlist
                      ? "glass text-accent hover:bg-white/10 hover:shadow-neon-purple"
                      : "bg-gradient-to-r from-accent to-blue-600 text-white shadow-neon-purple hover:shadow-neon-purple hover:-translate-y-1"
                  } disabled:opacity-50`}
                >
                  {isInWatchlist ? (
                    <>
                      <BookmarkCheck size={22} className="text-accent" />
                      In Watchlist
                    </>
                  ) : (
                    <>
                      <Bookmark size={22} />
                      Add to Watchlist
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="px-6 md:px-12 md:mt-24">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
          <div className="md:hidden glass-card p-2 rounded-3xl w-2/3 mx-auto -mt-32 z-20 relative">
            <img
              src={
                movie.poster_path
                  ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
                  : "https://via.placeholder.com/300x450?text=No+Image"
              }
              alt={movie.title}
              className="w-full rounded-2xl shadow-2xl"
            />
          </div>

          <div className="md:col-start-2 md:col-span-3 space-y-12">
            <div className="glass p-8 rounded-3xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-64 h-64 bg-accent/5 rounded-full blur-3xl -mr-32 -mt-32 transition-colors group-hover:bg-accent/10" />
              <h3 className="text-2xl font-heading font-bold text-white mb-4 flex items-center gap-3">
                <span className="w-1 h-6 bg-accent rounded-full"></span>
                Storyline
              </h3>
              <p className="text-lg text-gray-300 leading-relaxed font-medium">
                {movie.overview || "No overview available."}
              </p>

              {movie.genres && movie.genres.length > 0 && (
                <div className="mt-8 flex flex-wrap gap-3">
                  {movie.genres.map((genre) => (
                    <span
                      key={genre.id}
                      className="badge bg-white/5 hover:bg-white/10 transition-colors cursor-default"
                    >
                      {genre.name}
                    </span>
                  ))}
                </div>
              )}
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {movie.cast && movie.cast.length > 0 && (
                <div className="glass p-6 rounded-3xl">
                  <h4 className="text-xl font-heading font-bold text-white mb-4">
                    Top Cast
                  </h4>
                  <div className="space-y-3">
                    {movie.cast.slice(0, 5).map((actor) => (
                      <div key={actor.id} className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center text-gray-400 font-bold overflow-hidden">
                          {actor.profile_path ? (
                            <img
                              src={`https://image.tmdb.org/t/p/w200${actor.profile_path}`}
                              className="w-full h-full object-cover"
                            />
                          ) : (
                            actor.name.charAt(0)
                          )}
                        </div>
                        <div>
                          <p className="text-gray-200 font-semibold">
                            {actor.name}
                          </p>
                          {actor.character_name && (
                            <p className="text-sm text-gray-400">
                              {actor.character_name}
                            </p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {movie.crew && movie.crew.length > 0 && (
                <div className="glass p-6 rounded-3xl">
                  <h4 className="text-xl font-heading font-bold text-white mb-4">
                    Director
                  </h4>
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-full bg-white/10 flex items-center justify-center text-gray-400 font-bold text-lg overflow-hidden">
                      {movie.crew[0]?.profile_path ? (
                        <img
                          src={`https://image.tmdb.org/t/p/w200${movie.crew[0].profile_path}`}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        movie.crew[0]?.name.charAt(0)
                      )}
                    </div>
                    <p className="text-lg text-gray-200 font-semibold">
                      {movie.crew[0]?.name || "Unknown"}
                    </p>
                  </div>

                  {movie.keywords && movie.keywords.length > 0 && (
                    <div className="mt-8">
                      <h4 className="text-xl font-heading font-bold text-white mb-4">
                        Tags
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {movie.keywords.slice(0, 8).map((keyword) => (
                          <span
                            key={keyword.id}
                            className="text-xs font-semibold px-3 py-1 bg-white/5 text-gray-400 rounded-lg border border-white/5"
                          >
                            #{keyword.name.replace(/\s+/g, "")}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {movie.watch_providers && movie.watch_providers.length > 0 && (
        <div>
          <h3 className="text-2xl font-bold text-gray-100 mb-4">
            Where to Watch
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {movie.watch_providers.map((provider) => (
              <ProviderBadge
                key={`${provider.provider_id}-${provider.access_type}`}
                provider={provider}
              />
            ))}
          </div>
        </div>
      )}

      {similar.length > 0 && (
        <div>
          <MovieRow title="Similar Movies" movies={similar} />
          {similar[0]?.recommendation_reason && (
            <div className="mt-6 space-y-4">
              {similar.slice(0, 3).map((rec) => (
                <RecommendationExplanation
                  key={rec.id}
                  reasons={rec.recommendation_reason}
                  similarityScore={rec.similarity_score}
                />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
