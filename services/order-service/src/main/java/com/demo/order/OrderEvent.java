package com.demo.order;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public record OrderEvent(
    String event,
    String version,
    Long orderId,
    Long userId,
    BigDecimal total,
    LocalDateTime timestamp
) {
    public static OrderEvent created(Order order) {
        return new OrderEvent(
            "order.created",
            "1.0",
            order.getId(),
            order.getUserId(),
            order.getTotal(),
            order.getCreatedAt()
        );
    }
}