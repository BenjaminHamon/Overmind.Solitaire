using System.Collections.Generic;

namespace Overmind.Solitaire.UnityClient.Editor
{
	public static class EditorCommand
	{
		public static void BuildAssetBundles()
		{
			EditorCommandHelpers.ConfigureLogging();

			Dictionary<string, string> arguments = EditorCommandHelpers.FindMethodArguments();
			string platform = EditorCommandHelpers.ParseArgument<string>(arguments, "platform");
			string assetBundleDirectory = EditorCommandHelpers.ParseArgument<string>(arguments, "assetBundleDirectory");

			AssetBundleBuilder.BuildAllAssetBundles(platform, assetBundleDirectory);
		}

		public static void BuildPackage()
		{
			EditorCommandHelpers.ConfigureLogging();

			Dictionary<string, string> arguments = EditorCommandHelpers.FindMethodArguments();
			string platform = EditorCommandHelpers.ParseArgument<string>(arguments, "platform");
			string configuration = EditorCommandHelpers.ParseArgument<string>(arguments, "configuration");
			string assetBundleDirectory = EditorCommandHelpers.ParseArgument<string>(arguments, "assetBundleDirectory");
			string packageDirectory = EditorCommandHelpers.ParseArgument<string>(arguments, "packageDirectory");

			PackageBuilder.BuildPackage(platform, configuration, assetBundleDirectory, packageDirectory);
		}
	}
}
