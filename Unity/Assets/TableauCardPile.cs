using System.Collections.Generic;
using System.Linq;

namespace Overmind.Solitaire.Unity
{
	/// <summary>The tableau is the main area, where the player can place cards as sequences of alternating color and reveal hidden cards.</summary>
	public class TableauCardPile : CardPile
	{
		public int CardMaxNumber;

		public override bool TryPush(Card card)
		{
			Card topCard = Cards.FirstOrDefault();
			bool canPushAsFirstCard = (topCard == null) && (card.Number == CardMaxNumber);
			bool canPushAsNextCard = (topCard != null) && topCard.Visible && (topCard.Type.ToColor() != card.Type.ToColor()) && (topCard.Number == card.Number + 1);

			if (canPushAsFirstCard || canPushAsNextCard)
			{
				Push(card);
				return true;
			}

			return false;
		}

		public bool CanReveal(Card card)
		{
			return Cards.FirstOrDefault() == card;
		}

		public IEnumerable<Card> GetChildren(Card baseCard)
		{
			return Cards.TakeWhile(card => card != baseCard).Reverse();
		}
	}
}
