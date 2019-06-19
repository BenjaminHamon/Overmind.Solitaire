using System;
using System.Collections.Generic;
using System.IO;
using UnityEditor;

namespace Overmind.Solitaire.UnityClient.Editor
{
	public static class PackageBuilder
	{
		public static void GeneratePackage()
		{
			Dictionary<string, string> arguments = EditorCommandHelpers.FindMethodArguments();
			string platform = EditorCommandHelpers.ParseArgument<string>(arguments, "platform");
			string configuration = EditorCommandHelpers.ParseArgument<string>(arguments, "configuration");
			string destination = EditorCommandHelpers.ParseArgument<string>(arguments, "destination");

			GeneratePackage(platform, configuration, destination);
		}

		public static void GeneratePackage(string platform, string configuration, string destination)
		{
			UnityEngine.Debug.LogFormat("[PackageBuilder] Packaging for platform '{0}' with configuration '{1}'", platform, configuration);
			UnityEngine.Debug.LogFormat("[PackageBuilder] Writing package to '{0}'", destination);

			BuildTarget unityPlatform = ConvertPlatform(platform);
			BuildOptions options = GetOptions(configuration);
			string packagePath = BuildPackagePath(unityPlatform, destination, Application.ApplicationFullName);
			List<string> sceneCollection = new List<string>() { "Assets/MenuScene.unity", "Assets/GameScene.unity" };

			BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions()
			{
				target = unityPlatform,
				options = options,
				locationPathName = packagePath,
				scenes = sceneCollection.ToArray(),
			};

			BuildPipeline.BuildPlayer(buildPlayerOptions);
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
				case "Debug": return BuildOptions.Development;
				case "Release": return BuildOptions.None;
				default: throw new ArgumentException(String.Format("Unknown configuration: '{0}'", configuration));
			}
		}

		private static string BuildPackagePath(BuildTarget platform, string path, string application)
		{
			switch (platform)
			{
				case BuildTarget.Android: return path + ".apk";
				case BuildTarget.StandaloneLinux64: return Path.Combine(path, application);
				case BuildTarget.StandaloneWindows64: return Path.Combine(path, application + ".exe");
				default: throw new ArgumentException(String.Format("Unsupported platform: '{0}'", platform));
			}
		}
	}
}