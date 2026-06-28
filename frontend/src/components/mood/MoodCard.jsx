import { useNavigate } from "react-router-dom";

export default function MoodCard({ mood }) {
  const moodEmojis = {
    Happy: "😊",
    Emotional: "😢",
    Romantic: "💕",
    "Mind-Bending": "🤯",
    "Dark Thriller": "🌑",
    Inspirational: "🚀",
    "Feel-Good": "🌟",
    "Action-Packed": "💥",
    Motivational: "💪",
  };

  const emoji = moodEmojis[mood.name] || "🎬";
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/moods?mood=${encodeURIComponent(mood.name)}`);
  };

  return (
    <div onClick={handleClick}>
      <div className="card p-8 text-center hover:shadow-xl transition-colors cursor-pointer h-32 flex flex-col items-center justify-center hover:bg-gray-700 transition-colors">
        <div className="text-5xl mb-3">{emoji}</div>
        <h3 className="text-xl font-semibold text-gray-100 hover:text-accent transition-colors">
          {mood.name}
        </h3>
      </div>
    </div>
  );
}
