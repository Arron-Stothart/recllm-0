interface Preference {
  category: string
  description: string
}

export function UserProfile() {
  const preferences: Preference[] = []

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2 className="text-2xl font-semibold text-gray-900 mb-4">Your Profile</h2>
      
      <div className="space-y-6">
        {/* Learned Preferences */}
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Learned Preferences
          </h3>
          {preferences.length > 0 ? (
            <ul className="space-y-2">
              {preferences.map((pref, index) => (
                <li key={index} className="bg-gray-50 rounded-lg p-3">
                  <span className="font-medium text-gray-700">{pref.category}:</span>
                  <p className="text-gray-600 text-sm mt-1">{pref.description}</p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500 text-sm">
              Your preferences will appear here as you interact with the system
            </p>
          )}
        </div>

        {/* Recent Interactions */}
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Recent Interactions
          </h3>
          <div className="bg-gray-50 rounded-lg p-3">
            <p className="text-gray-500 text-sm">
              Your recent interactions will be shown here
            </p>
          </div>
        </div>

        {/* Settings */}
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Settings</h3>
          <div className="space-y-2">
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                className="rounded border-gray-300 text-blue-500 focus:ring-blue-500"
              />
              <span className="text-sm text-gray-700">Remember conversation history</span>
            </label>
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                className="rounded border-gray-300 text-blue-500 focus:ring-blue-500"
              />
              <span className="text-sm text-gray-700">Use preferences for recommendations</span>
            </label>
          </div>
        </div>
      </div>
    </div>
  )
} 