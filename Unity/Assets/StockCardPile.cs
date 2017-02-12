using System.Linq;

namespace Overmind.Solitaire.Unity
{
	public class StockCardPile : CardPile
	{
		public WasteCardPile Waste;

		public void OnMouseUp()
		{
			if (Cards.Any())
				Waste.Push(Cards.Peek());
			else
			{
				Card card = Waste.Peek();
				while (card != null)
				{
					Push(card);
					card = Waste.Peek();
				}
			}
		}

		protected override void DoPush(Card card)
		{
			base.DoPush(card);
			card.Visible = false;
			card.Collider.enabled = false;
		}
	}
}
