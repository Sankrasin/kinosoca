export default function ProviderBadge({ provider }) {
  const logoUrl = provider.logo_path
    ? `https://image.tmdb.org/t/p/w92${provider.logo_path}`
    : null;

  const content = (
    <div className="flex items-center gap-2 p-2 bg-secondary rounded-lg hover:bg-gray-600 transition-colors cursor-pointer">
      {logoUrl ? (
        <img src={logoUrl} alt={provider.name} className="w-8 h-8 rounded" />
      ) : (
        <div className="w-8 h-8 bg-gray-700 rounded flex items-center justify-center text-xs font-bold">
          {provider.name.charAt(0)}
        </div>
      )}
      <div>
        <p className="text-sm font-medium text-gray-100">{provider.name}</p>
        <p className="text-xs text-gray-400 capitalize">
          {provider.access_type}
        </p>
      </div>
    </div>
  );

  if (provider.provider_url) {
    return (
      <a href={provider.provider_url} target="_blank" rel="noopener noreferrer">
        {content}
      </a>
    );
  }

  return content;
}
