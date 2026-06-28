import { Lightbulb } from "lucide-react";

export default function RecommendationExplanation({
  reasons,
  similarityScore,
}) {
  if (!reasons || reasons.length === 0) {
    return null;
  }

  return (
    <div className="mt-4 p-3 bg-primary rounded-lg border border-secondary">
      <div className="flex items-start gap-2">
        <Lightbulb size={18} className="text-yellow-400 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <p className="text-sm font-semibold text-gray-100 mb-2">
            Recommended because:
          </p>
          <ul className="text-sm text-gray-300 space-y-1">
            {reasons.map((reason, index) => (
              <li key={index} className="flex items-start gap-2">
                <span className="text-accent mt-0.5">•</span>
                <span>{reason}</span>
              </li>
            ))}
          </ul>
          {similarityScore && (
            <p className="text-xs text-gray-400 mt-2">
              Match score: {(similarityScore * 100).toFixed(0)}%
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
