using System;
using System.IO;
using UnityEngine;

namespace Overmind.Solitaire.UnityClient.Content
{
	public class ResourceLoader : IAssetLoader<UnityEngine.Object>
	{
		public TAsset LoadByPath<TAsset>(string path) where TAsset : UnityEngine.Object
		{
			return Resources.Load<TAsset>(path) ?? throw new FileNotFoundException(String.Format("Asset not found for path '{0}'", path));
		}

		public TAsset LoadOrDefaultByPath<TAsset>(string path) where TAsset : UnityEngine.Object
		{
			return Resources.Load<TAsset>(path);
		}
	}
}
