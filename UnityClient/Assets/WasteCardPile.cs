namespace Overmind.Solitaire.UnityClient
{
	/// <summary>The waste is the card pile where cards drawn from the stock are put.</summary>
	public class WasteCardPile : CardPile
	{
		protected override void DoPush(Card card)
		{
			base.DoPush(card);

			card.Visible = true;
			card.Collider.enabled = true;
		}
	}
}
