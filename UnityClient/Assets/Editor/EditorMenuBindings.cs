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
			string assetBundleDirectory = Path.Combine("..", "Artifacts", "AssetBundles", "Android");
			AssetBundleBuilder.BuildAllAssetBundles("Android", assetBundleDirectory);
		}

		[MenuItem("Development/Asset Bundles/Build for Linux")]
		internal static void BuildAllAssetBundlesForLinux()
		{
			string assetBundleDirectory = Path.Combine("..", "Artifacts", "AssetBundles", "Linux");
			AssetBundleBuilder.BuildAllAssetBundles("Linux", assetBundleDirectory);
		}

		[MenuItem("Development/Asset Bundles/Build for Windows")]
		internal static void BuildAllAssetBundlesForWindows()
		{
			string assetBundleDirectory = Path.Combine("..", "Artifacts", "AssetBundles", "Windows");
			AssetBundleBuilder.BuildAllAssetBundles("Windows", assetBundleDirectory);
		}

		[MenuItem("Development/Package/Build for Android (Debug)")]
		internal static void BuildPackageForAndroidDebug()
		{
			string assetBundleDirectory = Path.Combine("..", "Artifacts", "AssetBundles", "Android");
			string packageDirectory = Path.Combine("..", "Artifacts", "Packages", "Android", "Debug");
			PackageBuilder.BuildPackage("Android", "Debug", assetBundleDirectory, packageDirectory);
			Process.Start(packageDirectory);
		}

		[MenuItem("Development/Package/Build for Android (Release)")]
		internal static void BuildPackageForAndroidRelease()
		{
			string assetBundleDirectory = Path.Combine("..", "Artifacts", "AssetBundles", "Android");
			string packageDirectory = Path.Combine("..", "Artifacts", "Packages", "Android", "Release");
			PackageBuilder.BuildPackage("Android", "Release", assetBundleDirectory, packageDirectory);
			Process.Start(packageDirectory);
		}

		[MenuItem("Development/Package/Build for Linux (Debug)")]
		internal static void BuildPackageForLinuxDebug()
		{
			string assetBundleDirectory = Path.Combine("..", "Artifacts", "AssetBundles", "Linux");
			string packageDirectory = Path.Combine("..", "Artifacts", "Packages", "Linux", "Debug");
			PackageBuilder.BuildPackage("Linux", "Debug", assetBundleDirectory, packageDirectory);
			Process.Start(packageDirectory);
		}

		[MenuItem("Development/Package/Build for Linux (Release)")]
		internal static void BuildPackageForLinuxRelease()
		{
			string assetBundleDirectory = Path.Combine("..", "Artifacts", "AssetBundles", "Linux");
			string packageDirectory = Path.Combine("..", "Artifacts", "Packages", "Linux", "Release");
			PackageBuilder.BuildPackage("Linux", "Release", assetBundleDirectory, packageDirectory);
			Process.Start(packageDirectory);
		}

		[MenuItem("Development/Package/Build for Windows (Debug)")]
		internal static void BuildPackageForWindowsDebug()
		{
			string assetBundleDirectory = Path.Combine("..", "Artifacts", "AssetBundles", "Windows");
			string packageDirectory = Path.Combine("..", "Artifacts", "Packages", "Windows", "Debug");
			PackageBuilder.BuildPackage("Windows", "Debug", assetBundleDirectory, packageDirectory);
			Process.Start(packageDirectory);
		}

		[MenuItem("Development/Package/Build for Windows (Release)")]
		internal static void BuildPackageForWindowsRelease()
		{
			string assetBundleDirectory = Path.Combine("..", "Artifacts", "AssetBundles", "Windows");
			string packageDirectory = Path.Combine("..", "Artifacts", "Packages", "Windows", "Release");
			PackageBuilder.BuildPackage("Windows", "Release", assetBundleDirectory, packageDirectory);
			Process.Start(packageDirectory);
		}
	}
}
