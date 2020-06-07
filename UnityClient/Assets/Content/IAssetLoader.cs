namespace Overmind.Solitaire.UnityClient.Content
{
	public interface IAssetLoader<TAssetBase>
	{
		void LoadBundle(string bundle);
		void UnloadBundle(string bundle);

		TAsset LoadByPath<TAsset>(string bundle, string path) where TAsset : TAssetBase;
		TAsset LoadOrDefaultByPath<TAsset>(string bundle, string path) where TAsset : TAssetBase;
		TAsset LoadPlaceholder<TAsset>() where TAsset : TAssetBase;
	}
}
