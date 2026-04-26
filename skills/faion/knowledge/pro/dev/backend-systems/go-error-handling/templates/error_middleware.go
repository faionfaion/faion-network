// internal/middleware/errors.go
// Gin middleware: maps AppError (or any error) to a structured JSON response.
// Register as a global middleware BEFORE route definitions.
package middleware

import (
	"net/http"

	"github.com/gin-gonic/gin"

	"project/internal/apperror"
)

// ErrorHandler converts errors appended via c.Error(err) into JSON responses.
// Handlers must NOT call c.JSON for error paths — they call c.Error() and return.
func ErrorHandler() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Next()

		if len(c.Errors) == 0 {
			return
		}

		err := c.Errors.Last().Err

		if appErr, ok := err.(*apperror.AppError); ok {
			c.JSON(appErr.HTTPStatus, gin.H{
				"error": gin.H{
					"code":    appErr.Code,
					"message": appErr.Message,
				},
			})
			return
		}

		// Unrecognized error — log it, return a safe 500.
		// Use your structured logger here; err.Error() MUST NOT reach the client.
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": gin.H{
				"code":    "INTERNAL_ERROR",
				"message": "An unexpected error occurred",
			},
		})
	}
}
