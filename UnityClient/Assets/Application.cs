using Overmind.Solitaire.UnityClient.Content;

namespace Overmind.Solitaire.UnityClient
{
	/// <summary>Global static class to keep state between scenes.</summary>
	public static class Application
	{
		public static string ApplicationTitle { get { return "Overmind Solitaire"; } }
		public static string ApplicationFullName { get { return "Overmind.Solitare.UnityClient"; } }

		public static IAssetLoader<UnityEngine.Object> AssetLoader = new ResourceLoader();

		public static int? GameSeed;
	}
}
