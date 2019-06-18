using System.Linq;

namespace Overmind.Solitaire.UnityClient
{
	/// <summary>The stock is the pile with the leftover cards from the setup, from which the player can draw.</summary>
	public class StockCardPile : CardPile
	{
		public WasteCardPile Waste;

		public void OnMouseUp()
		{
			if (Cards.Any())
			{
				Draw();
			}
			else
			{
				ResetFromWaste();
			}
		}

		private void Draw()
		{
			Waste.Push(Cards.Peek());
		}

		private void ResetFromWaste()
		{
			Card card = Waste.Peek();

			while (card != null)
			{
				Push(card);
				card = Waste.Peek();
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
