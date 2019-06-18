using System;

namespace Overmind.Solitaire.UnityClient
{
	public enum CardType
	{
		Unknown,
		Clubs,
		Diamonds,
		Hearts,
		Spades,
	}

	public enum CardColor
	{
		Unknown,
		Black,
		Red,
	}

	public static class CardTypeExtensions
	{
		public static CardColor ToColor(this CardType type)
		{
			switch (type)
			{
				case CardType.Clubs: return CardColor.Black;
				case CardType.Diamonds: return CardColor.Red;
				case CardType.Hearts: return CardColor.Red;
				case CardType.Spades: return CardColor.Black;
				default: throw new ArgumentException(String.Format("Unsupported card type: '{0}'", type));
			}
		}
	}
}
