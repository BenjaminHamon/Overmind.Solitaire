using System;
using System.IO;
using UnityEditor;

namespace Overmind.Solitaire.UnityClient.Editor
{
	public static class AssetBundleBuilder
	{
		[MenuItem("Development/Build AssetBundles for Windows")]
		internal static void BuildAllAssetBundlesForWindows()
		{
			BuildAllAssetBundles("Windows", Path.Combine("AssetBundles", "Windows"));
		}

		public static void BuildAllAssetBundles(string platform, string outputPath)
		{
			BuildTarget unityPlatform = ConvertPlatform(platform);
			BuildAssetBundleOptions options = BuildAssetBundleOptions.StrictMode | BuildAssetBundleOptions.DeterministicAssetBundle;

			Directory.CreateDirectory(outputPath);
			BuildPipeline.BuildAssetBundles(outputPath, options, unityPlatform);
			AssetDatabase.Refresh();
		}

		private static BuildTarget ConvertPlatform(string platform)
		{
			switch (platform)
			{
				case "Android": return BuildTarget.Android;
				case "Linux": return BuildTarget.StandaloneLinux64;
				case "Windows": return BuildTarget.StandaloneWindows64;
				default: throw new ArgumentException(String.Format("Unsupported platform: '{0}'", platform));
			}
		}
	}
}
