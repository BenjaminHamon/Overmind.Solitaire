using System.Diagnostics;
using System.IO;
using UnityEditor;

namespace Overmind.Solitaire.UnityClient.Editor
{
	internal static class EditorMenuBindings
	{
		[MenuItem("Development/Asset Bundles/Build for Android")]
		internal static void BuildAllAssetBundlesForAndroid()
		{
			AssetBundleBuilder.BuildAllAssetBundles("Android", Path.Combine("AssetBundles", "Android"));
		}

		[MenuItem("Development/Asset Bundles/Build for Linux")]
		internal static void BuildAllAssetBundlesForLinux()
		{
			AssetBundleBuilder.BuildAllAssetBundles("Linux", Path.Combine("AssetBundles", "Linux"));
		}

		[MenuItem("Development/Asset Bundles/Build for Windows")]
		internal static void BuildAllAssetBundlesForWindows()
		{
			AssetBundleBuilder.BuildAllAssetBundles("Windows", Path.Combine("AssetBundles", "Windows"));
		}

		[MenuItem("Development/Package/Build for Android (Debug)")]
		internal static void BuildPackageForAndroidDebug()
		{
			string packagePath = Path.Combine("..", "Artifacts", "Packages", "Android", "Debug");
			PackageBuilder.GeneratePackage("Android", "Debug", packagePath);
			Process.Start(packagePath);
		}

		[MenuItem("Development/Package/Build for Android (Release)")]
		internal static void BuildPackageForAndroidRelease()
		{
			string packagePath = Path.Combine("..", "Artifacts", "Packages", "Android", "Release");
			PackageBuilder.GeneratePackage("Android", "Release", packagePath);
			Process.Start(packagePath);
		}

		[MenuItem("Development/Package/Build for Linux (Debug)")]
		internal static void BuildPackageForLinuxDebug()
		{
			string packagePath = Path.Combine("..", "Artifacts", "Packages", "Linux", "Debug");
			PackageBuilder.GeneratePackage("Linux", "Debug", packagePath);
			Process.Start(packagePath);
		}

		[MenuItem("Development/Package/Build for Linux (Release)")]
		internal static void BuildPackageForLinuxRelease()
		{
			string packagePath = Path.Combine("..", "Artifacts", "Packages", "Linux", "Release");
			PackageBuilder.GeneratePackage("Linux", "Release", packagePath);
			Process.Start(packagePath);
		}

		[MenuItem("Development/Package/Build for Windows (Debug)")]
		internal static void BuildPackageForWindowsDebug()
		{
			string packagePath = Path.Combine("..", "Artifacts", "Packages", "Windows", "Debug");
			PackageBuilder.GeneratePackage("Windows", "Debug", packagePath);
			Process.Start(packagePath);
		}

		[MenuItem("Development/Package/Build for Windows (Release)")]
		internal static void BuildPackageForWindowsRelease()
		{
			string packagePath = Path.Combine("..", "Artifacts", "Packages", "Windows", "Release");
			PackageBuilder.GeneratePackage("Windows", "Release", packagePath);
			Process.Start(packagePath);
		}
	}
}
