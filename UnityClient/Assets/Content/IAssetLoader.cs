namespace Overmind.Solitaire.UnityClient.Content
{
	// About asset loaders

	// There are several ways to load assets with Unity,
	// thus several implementations of the IAssetLoader interface.

	// - EditorAssetLoader
	// Use EditorAssetLoader to use the asset database from the Unity Editor.
	// It is only available in the editor and can load any asset in the project.

	// - AssetLoaderUsingResources
	// Use AssetLoaderUsingResources to use the Unity resource system.
	// This is the quick and easy solution, and works the same way in editor and in standalone.
	// All assets under Resources directories are included in the game package and thus available at runtime.
	// See https://docs.unity3d.com/ScriptReference/Resources.html

	// - AssetLoaderUsingBundles
	// Use AssetLoaderUsingBundles to use the Unity asset bundles.
	// The Unity project must be setup with the AssetBundle package.
	// Assets must be associated with asset bundles.
	// Asset bundles must be built for each platform and included with the game package.
	// See https://docs.unity3d.com/Manual/AssetBundles-Workflow.html

	// See also Unity Addressable Asset system
	// https://docs.unity3d.com/Packages/com.unity.addressables@1.9/manual/index.html

	public interface IAssetLoader<TAssetBase>
	{
		void LoadBundle(string bundle);
		void UnloadBundle(string bundle);

		TAsset LoadByPath<TAsset>(string bundle, string path) where TAsset : TAssetBase;
		TAsset LoadOrDefaultByPath<TAsset>(string bundle, string path) where TAsset : TAssetBase;
		TAsset LoadPlaceholder<TAsset>() where TAsset : TAssetBase;
	}
}
