namespace Overmind.Solitaire.Unity
{
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
