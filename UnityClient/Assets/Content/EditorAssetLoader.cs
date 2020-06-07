#if UNITY_EDITOR

using System;
using System.IO;
using UnityEditor;
using UnityEngine;

namespace Overmind.Solitaire.UnityClient.Content
{
	public class EditorAssetLoader : IAssetLoader<UnityEngine.Object>
	{
		public void LoadBundle(string bundle) {}
		public void UnloadBundle(string bundle) {}

		public TAsset LoadByPath<TAsset>(string bundle, string path) where TAsset : UnityEngine.Object
		{
			return AssetDatabase.LoadAssetAtPath<TAsset>("Assets" + "/" + path)
				?? throw new FileNotFoundException(String.Format("Asset not found (Path: '{0}')", path));
		}

		public TAsset LoadOrDefaultByPath<TAsset>(string bundle, string path) where TAsset : UnityEngine.Object
		{
			return AssetDatabase.LoadAssetAtPath<TAsset>("Assets" + "/" + path) ?? LoadPlaceholder<TAsset>();
		}

		public TAsset LoadPlaceholder<TAsset>() where TAsset : UnityEngine.Object
		{
			return Resources.Load<TAsset>("Placeholder");
		}
	}
}

#endif // UNITY_EDITOR
