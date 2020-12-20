using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using UnityEditor;
using UnityEditor.Build.Reporting;

namespace Overmind.Solitaire.UnityClient.Editor
{
	public static class PackageBuilder
	{
		public static void GeneratePackage()
		{
			Dictionary<string, string> arguments = EditorCommandHelpers.FindMethodArguments();
			string platform = EditorCommandHelpers.ParseArgument<string>(arguments, "platform");
			string configuration = EditorCommandHelpers.ParseArgument<string>(arguments, "configuration");
			string assetBundleDirectory = EditorCommandHelpers.ParseArgument<string>(arguments, "assetBundleDirectory");
			string packageDirectory = EditorCommandHelpers.ParseArgument<string>(arguments, "packageDirectory");

			GeneratePackage(platform, configuration, assetBundleDirectory, packageDirectory);
		}

		public static void GeneratePackage(string platform, string configuration, string assetBundleDirectory, string packageDirectory)
		{
			UnityEngine.Debug.LogFormat("[PackageBuilder] Packaging for platform '{0}' with configuration '{1}'", platform, configuration);
			UnityEngine.Debug.LogFormat("[PackageBuilder] Writing package to '{0}'", packageDirectory);

			BuildTarget unityPlatform = ConvertPlatform(platform);
			BuildOptions options = GetOptions(configuration);
			string packagePath = BuildPackagePath(unityPlatform, packageDirectory, Application.ApplicationFullName);
			List<string> sceneCollection = new List<string>() { "Assets/MenuScene.unity", "Assets/GameScene.unity" };

			BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions()
			{
				target = unityPlatform,
				options = options,
				locationPathName = packagePath,
				scenes = sceneCollection.ToArray(),
			};

			BuildReport buildReport = BuildPipeline.BuildPlayer(buildPlayerOptions);

			if (buildReport.summary.result == BuildResult.Succeeded)
			{
				CopyAssetBundles(platform, assetBundleDirectory, packageDirectory);
			}

			UnityEngine.Debug.LogFormat("[PackageBuilder] Build completed with status '{0}' ({1} errors, {2} warnings)",
				buildReport.summary.result, buildReport.summary.totalErrors, buildReport.summary.totalWarnings);

			if (buildReport.summary.result == BuildResult.Failed)
				throw new Exception("Build failed");
		}

		public static void CopyAssetBundles(string platform, string assetBundleDirectory, string packageDirectory)
		{
			UnityEngine.Debug.LogFormat("[PackageBuilder] Copying asset bundles");

			List<string> allFiles = Directory.EnumerateFiles(assetBundleDirectory, "*", SearchOption.AllDirectories)
				.Where(filePath => Path.GetExtension(filePath) != ".meta")
				.Select(filePath => Regex.Replace(filePath, "^" + Regex.Escape(assetBundleDirectory + Path.DirectorySeparatorChar), ""))
				.ToList();

			if (Directory.Exists(Path.Combine(packageDirectory, "AssetBundles")))
				Directory.Delete(Path.Combine(packageDirectory, "AssetBundles"), true);

			foreach (string sourcePath in allFiles)
			{
				string source = Path.Combine(assetBundleDirectory, sourcePath);
				string destination = Path.Combine(packageDirectory, "AssetBundles", sourcePath);

				// UnityEngine.Debug.LogFormat("[PackageBuilder] + '{0}' => '{1}'", source, destination);

				Directory.CreateDirectory(Path.GetDirectoryName(destination));
				File.Copy(source, destination);
			}
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

		private static BuildOptions GetOptions(string configuration)
		{
			switch (configuration)
			{
				case "Debug": return BuildOptions.StrictMode | BuildOptions.Development | BuildOptions.AllowDebugging;
				case "Release": return BuildOptions.StrictMode;
				default: throw new ArgumentException(String.Format("Unknown configuration: '{0}'", configuration));
			}
		}

		private static string BuildPackagePath(BuildTarget platform, string path, string application)
		{
			switch (platform)
			{
				case BuildTarget.Android: return Path.Combine(path, application + ".apk");
				case BuildTarget.StandaloneLinux64: return Path.Combine(path, application);
				case BuildTarget.StandaloneWindows64: return Path.Combine(path, application + ".exe");
				default: throw new ArgumentException(String.Format("Unsupported platform: '{0}'", platform));
			}
		}
	}
}