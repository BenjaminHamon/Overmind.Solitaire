using System;
using System.IO;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEngine;

namespace Overmind.Solitaire.UnityClient.Editor
{
	public static class AssetBundleBuilder
	{
		public static void BuildAllAssetBundles(string platform, string assetBundleDirectory)
		{
			UnityEngine.Debug.LogFormat("[AssetBundleBuilder] Building asset bundles for platform '{0}'", platform);
			UnityEngine.Debug.LogFormat("[AssetBundleBuilder] Writing to '{0}'", assetBundleDirectory);

			BuildTarget unityPlatform = ConvertPlatform(platform);
			BuildAssetBundleOptions options = BuildAssetBundleOptions.StrictMode | BuildAssetBundleOptions.DeterministicAssetBundle;

			Directory.CreateDirectory(assetBundleDirectory);
			AssetBundleManifest manifest = BuildPipeline.BuildAssetBundles(assetBundleDirectory, options, unityPlatform);
			BuildResult result = manifest != null ? BuildResult.Succeeded : BuildResult.Failed;
			AssetDatabase.Refresh();

			UnityEngine.Debug.LogFormat("[PackageBuilder] Build completed with status '{0}'", result);

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
