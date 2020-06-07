#if UNITY_EDITOR

using System;
using System.IO;
using UnityEditor;
using UnityEngine;

namespace Overmind.Solitaire.UnityClient.Content
{
	public class EditorAssetLoader : IAssetLoader<UnityEngine.Object>
	{
		public TAsset LoadByPath<TAsset>(string path) where TAsset : UnityEngine.Object
		{
			return AssetDatabase.LoadAssetAtPath<TAsset>("Assets" + "/" + path)
				?? throw new FileNotFoundException(String.Format("Asset not found for path '{0}'", path));
		}

		public TAsset LoadOrDefaultByPath<TAsset>(string path) where TAsset : UnityEngine.Object
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
