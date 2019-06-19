namespace Overmind.Solitaire.UnityClient.Editor
{
	public static class EditorCommand
	{
		public static void GeneratePackage() { EditorCommandHelpers.ConfigureLogging(); PackageBuilder.GeneratePackage(); }
	}
}
