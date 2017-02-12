using System.Collections.Generic;
using System.Linq;

namespace Overmind.Solitaire.Unity
{
	public class TableauCardPile : CardPile
	{
		public int CardMaxNumber;

		public override bool TryPush(Card card)
		{
			Card topCard = Cards.FirstOrDefault();
			if (((topCard == null) && (card.Number == CardMaxNumber))
				|| ((topCard != null) && topCard.Visible && AreTypeCompatible(topCard.Type, card.Type) && (topCard.Number == card.Number + 1)))
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

		private bool AreTypeCompatible(CardType first, CardType second)
		{
			switch (first)
			{
				case CardType.Clubs:
				case CardType.Spades:
					return (second == CardType.Diamonds) || (second == CardType.Hearts);
				case CardType.Diamonds:
				case CardType.Hearts:
					return (second == CardType.Clubs) || (second == CardType.Spades);
				default:
					return false;
			}
		}
	}
}
