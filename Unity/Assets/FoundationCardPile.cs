using System;
using System.Linq;

namespace Overmind.Solitaire.Unity
{
	public class FoundationCardPile : CardPile
	{
		public int CardMaxNumber;

		public event Action Completed;

		public bool IsComplete
		{
			get
			{
				Card topCard = Peek();
				return (topCard != null) && (topCard.Number == CardMaxNumber);
			}
		}

		public override bool TryPush(Card card)
		{
			if (card.Parent.Peek() != card)
				return false;

			Card topCard = Cards.FirstOrDefault();

			if (((topCard == null) && (card.Number == 1))
				|| ((topCard != null) && (topCard.Type == card.Type) && (topCard.Number == card.Number - 1)))
			{
				Push(card);
				return true;
			}
			return false;
		}

		protected override void DoPush(Card card)
		{
			base.DoPush(card);
			if (IsComplete)
			{
				Action completedHandler = Completed;
				if (completedHandler != null)
					completedHandler();
			}
		}
	}
}
