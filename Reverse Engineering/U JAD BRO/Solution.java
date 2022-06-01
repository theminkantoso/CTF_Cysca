public class Solution {
	private static final byte CIPHERED_BYTES[] = {
		30, 0, 21, 8, 90, 86, 4, 0, 10, 6,
		80, 92, 38, 53, 30, 26, 80, 88, 113, 87,
		67
	};
	public static String cipherString(String text, String key) {
	StringBuilder sb = new StringBuilder();
	for (int i = 0; i < text.length(); i++) {
		sb.append((char)(text.charAt(i) ^ key.charAt(i % key.length())));
		}
	return sb.toString();
	}
	public static void main(String[] args) {
		String result;
		result = cipherString(new String(CIPHERED_BYTES), "Hero33");
		System.out.println(result);
	}
}