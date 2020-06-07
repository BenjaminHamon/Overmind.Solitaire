using System;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

namespace Overmind.Solitaire.UnityClient.Content
{
	public class AssetLoaderUsingBundles : IAssetLoader<UnityEngine.Object>
	{
		public AssetLoaderUsingBundles(string bundleDirectory)
		{
			this.bundleDirectory = bundleDirectory;
		}

		private string bundleDirectory;
		private Dictionary<string, AssetBundle> loadedBundles = new Dictionary<string, AssetBundle>();

		public void LoadBundle(string bundle)
		{
			if (loadedBundles.ContainsKey(bundle))
				return;

			string assetBundlePath = Path.Combine(bundleDirectory, bundle);
			AssetBundle assetBundle = AssetBundle.LoadFromFile(assetBundlePath)
				?? throw new FileNotFoundException(String.Format("Asset bundle not found (Path: '{0}')", assetBundlePath));

			loadedBundles.Add(bundle, assetBundle);
		}

		public void UnloadBundle(string bundle)
		{
			if (loadedBundles.ContainsKey(bundle) == false)
				return;

			AssetBundle assetBundle = loadedBundles[bundle];
			loadedBundles.Remove(bundle);
			assetBundle.Unload(true);
		}

		public TAsset LoadByPath<TAsset>(string bundle, string path) where TAsset : UnityEngine.Object
		{
			return loadedBundles[bundle].LoadAsset<TAsset>("Assets" + "/" + path)
				?? throw new FileNotFoundException(String.Format("Asset not found (Path: '{0}')", path));
		}

		public TAsset LoadOrDefaultByPath<TAsset>(string bundle, string path) where TAsset : UnityEngine.Object
		{
			if (loadedBundles.ContainsKey(bundle) == false)
				return LoadPlaceholder<TAsset>();
			return loadedBundles[bundle].LoadAsset<TAsset>("Assets" + "/" + path) ?? LoadPlaceholder<TAsset>();
		}

		public TAsset LoadPlaceholder<TAsset>() where TAsset : UnityEngine.Object
		{
			return Resources.Load<TAsset>("Placeholder");
		}
	}
}
