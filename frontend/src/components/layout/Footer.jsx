export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-primary border-t border-secondary mt-12">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div>
            <h3 className="text-xl font-bold text-accent mb-4">Kinosoca</h3>
            <p className="text-gray-400">
              Discover movies, find where to stream, and get AI-powered recommendations.
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-gray-100 mb-4">Quick Links</h4>
            <ul className="space-y-2 text-gray-400">
              <li>
                <a href="/" className="hover:text-accent transition-colors">
                  Home
                </a>
              </li>
              <li>
                <a href="/search" className="hover:text-accent transition-colors">
                  The Observatory
                </a>
              </li>
              <li>
                <a href="/moods" className="hover:text-accent transition-colors">
                  Moods
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  )
}