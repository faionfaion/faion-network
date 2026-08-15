// purpose: named ThreadPoolTaskExecutor + @Async configuration per async-via-named-executor rule
// consumes: pool-size config from application.yml
// produces: Spring config bean defining the executor + @Async target bean
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~250 tokens when loaded as reference

package faion.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.stereotype.Service;

import java.util.concurrent.Executor;

@Configuration
@EnableAsync
public class AsyncConfig {

    @Bean(name = "emailExecutor")
    public Executor emailExecutor(
        @Value("${faion.email.pool.core-size:4}") int core,
        @Value("${faion.email.pool.max-size:16}") int max,
        @Value("${faion.email.pool.queue-capacity:1000}") int queue
    ) {
        ThreadPoolTaskExecutor exec = new ThreadPoolTaskExecutor();
        exec.setCorePoolSize(core);
        exec.setMaxPoolSize(max);
        exec.setQueueCapacity(queue);
        exec.setThreadNamePrefix("email-");
        exec.initialize();
        return exec;
    }
}

@Service
class EmailSender {

    @Async("emailExecutor")
    public void sendOrderConfirmation(String to, String orderId) {
        // call SMTP / SES; if it throws, the executor logs.
    }
}
