import { Link } from "react-router-dom";
import { Star } from "lucide-react";

export default function MovieCard({ movie }) {
  const imageUrl = movie.poster_path
    ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
    : "https://via.placeholder.com/300x450?text=No+Image";

  return (
    <Link to={`/movie/${movie.id}`} className="group block w-full">
      <div className="relative rounded-2xl overflow-hidden aspect-[2/3] bg-secondary shadow-lg hover:shadow-accent/40 transition-all duration-300 hover:-translate-y-1 mb-3">
        <img
          src={imageUrl}
          alt={movie.title}
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
        />
      </div>

      <div className="px-1">
        <h3 className="font-heading font-bold text-lg text-white truncate group-hover:text-accent transition-colors duration-300">
          {movie.title}
        </h3>

        <div className="flex items-center justify-between mt-1">
          <span className="text-sm font-medium text-gray-400">
            {movie.release_year || "N/A"}
          </span>
          <div className="flex items-center gap-1">
            <Star size={14} className="text-accent fill-accent" />
            <span className="text-sm font-bold text-white">
              {movie.vote_average.toFixed(1)}
            </span>
          </div>
        </div>

        {movie.genres && movie.genres.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-2">
            {movie.genres.slice(0, 2).map((genre) => (
              <span
                key={genre.id}
                className="badge bg-white/5 text-gray-400 border-none px-2 py-0.5 text-[10px]"
              >
                {genre.name}
              </span>
            ))}
          </div>
        )}
      </div>
    </Link>
  );
}
