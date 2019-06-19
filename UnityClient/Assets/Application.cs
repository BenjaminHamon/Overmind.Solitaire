namespace Overmind.Solitaire.UnityClient
{
	/// <summary>Global static class to keep state between scenes.</summary>
	public static class Application
	{
		public static string ApplicationTitle { get { return "Overmind Solitaire"; } }
		public static string ApplicationFullName { get { return "Overmind.Solitare.UnityClient"; } }

		public static int? GameSeed;
	}
}
