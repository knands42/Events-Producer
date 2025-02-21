package org.example;

import java.util.Random;
import java.util.UUID;

public record Transaction(
        String transactionId,
        String userId,
        double amount,
        long transactionTime,
        String merchantId,
        String transactionType,
        String location,
        String paymentMethod,
        boolean isInternational,
        String currency) {

    private static final Random random = new Random();

    public static Transaction randomTransaction() {
        return new Transaction(
                UUID.randomUUID().toString(),
                String.valueOf(random.nextInt(100)),
                random.nextDouble(10, 100),
                System.currentTimeMillis(),
                String.valueOf(random.nextInt(50)),
                random.nextBoolean() ? "purchase" : "refund",
                random.nextBoolean() ? "NY, USA" : "LA, USA",
                random.nextBoolean() ? "credit_card" : "debit_card",
                random.nextBoolean(),
                random.nextBoolean() ? "USD" : "EUR");
    }
}