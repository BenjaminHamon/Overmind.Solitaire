using System;
using System.IO;
using UnityEngine;

namespace Overmind.Solitaire.UnityClient.Content
{
	public class AssetLoaderUsingResources : IAssetLoader<UnityEngine.Object>
	{
		public void LoadBundle(string bundle) { }
		public void UnloadBundle(string bundle) { }

		public TAsset LoadByPath<TAsset>(string bundle, string path) where TAsset : UnityEngine.Object
		{
			return Resources.Load<TAsset>(Path.ChangeExtension(path, null))
				?? throw new FileNotFoundException(String.Format("Asset not found (Path: '{0}')", path));
		}

		public TAsset LoadOrDefaultByPath<TAsset>(string bundle, string path) where TAsset : UnityEngine.Object
		{
			return Resources.Load<TAsset>(Path.ChangeExtension(path, null)) ?? LoadPlaceholder<TAsset>();
		}

		public TAsset LoadPlaceholder<TAsset>() where TAsset : UnityEngine.Object
		{
			return Resources.Load<TAsset>("Placeholder");
		}
	}
}
