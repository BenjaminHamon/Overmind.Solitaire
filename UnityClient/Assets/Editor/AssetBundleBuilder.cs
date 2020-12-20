using System;
using System.IO;
using UnityEditor;
using UnityEngine;

namespace Overmind.Solitaire.UnityClient.Editor
{
	public static class AssetBundleBuilder
	{
		public static void BuildAllAssetBundles(string platform, string outputPath)
		{
			BuildTarget unityPlatform = ConvertPlatform(platform);
			BuildAssetBundleOptions options = BuildAssetBundleOptions.StrictMode | BuildAssetBundleOptions.DeterministicAssetBundle;

			Directory.CreateDirectory(outputPath);
			AssetBundleManifest manifest = BuildPipeline.BuildAssetBundles(outputPath, options, unityPlatform);
			AssetDatabase.Refresh();

			if (manifest == null)
				throw new Exception("Build failed");
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
