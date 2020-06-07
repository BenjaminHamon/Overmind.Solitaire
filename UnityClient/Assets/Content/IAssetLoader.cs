namespace Overmind.Solitaire.UnityClient.Content
{
	public interface IAssetLoader<TAssetBase>
	{
		TAsset LoadByPath<TAsset>(string path) where TAsset : TAssetBase;
		TAsset LoadOrDefaultByPath<TAsset>(string path) where TAsset : TAssetBase;
	}
}
