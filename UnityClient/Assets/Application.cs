using Overmind.Solitaire.UnityClient.Content;
using System;
using System.IO;
using UnityEngine;

namespace Overmind.Solitaire.UnityClient
{
	/// <summary>Global static class to keep state between scenes.</summary>
	public static class Application
	{
		public static string ApplicationTitle { get { return "Overmind Solitaire"; } }
		public static string ApplicationFullName { get { return "Overmind.Solitare.UnityClient"; } }

		private static bool UseAssetBundlesInEditor = false;
		public static IAssetLoader<UnityEngine.Object> AssetLoader = CreateAssetLoader();

		public static int? GameSeed;

		private static IAssetLoader<UnityEngine.Object> CreateAssetLoader()
		{
#if UNITY_EDITOR
			if (UnityEngine.Application.isEditor)
			{
				if (UseAssetBundlesInEditor)
					return new AssetLoader(Path.Combine("AssetBundles", GetAssetBundlePlatform(UnityEngine.Application.platform)));

				return new EditorAssetLoader();
			}
#endif

			string installationDirectory = Path.GetDirectoryName(UnityEngine.Application.dataPath);
			return new AssetLoader(Path.Combine(installationDirectory, "AssetBundles"));
		}

		private static string GetAssetBundlePlatform(RuntimePlatform platform)
		{
			switch (platform)
			{
				case RuntimePlatform.Android: return "Android";
				case RuntimePlatform.LinuxEditor: return "Linux";
				case RuntimePlatform.LinuxPlayer: return "Linux";
				case RuntimePlatform.WindowsEditor: return "Windows";
				case RuntimePlatform.WindowsPlayer: return "Windows";
				default: throw new ArgumentException(String.Format("Unsupported platform: '{0}'", platform));
			}
		}
	}
}
