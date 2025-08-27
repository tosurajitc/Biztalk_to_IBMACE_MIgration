# ACE_MessageFlow_TestSuite - API Reference

## Overview
This document provides comprehensive API reference for the IBM ACE Message Flow endpoints covered by the Postman test collections.

**Generated:** 2025-08-27 21:51:46
**Message Flows**: 1

## Authentication
All endpoints require Bearer token authentication:
```
Authorization: Bearer {auth_token}
```

## Content Types
- **Request**: application/xml
- **Response**: application/xml or application/json (depending on configuration)

## Message Flow Endpoints

### Enterprise_MessageFlow



## Common Request Headers
```
Content-Type: application/xml
Authorization: Bearer {auth_token}
X-Test-Scenario: {test_scenario_id}
Accept: application/xml
```

## Common Response Codes
- **200**: Success - Request processed successfully
- **202**: Accepted - Request accepted for processing
- **400**: Bad Request - Invalid request format or data
- **401**: Unauthorized - Missing or invalid authentication
- **403**: Forbidden - Insufficient permissions
- **422**: Unprocessable Entity - Business logic validation failed
- **500**: Internal Server Error - Server processing error
- **503**: Service Unavailable - Service temporarily unavailable

## Error Response Format
```xml
<?xml version="1.0" encoding="UTF-8"?>
<ErrorResponse>
    <ErrorCode>ERR_001</ErrorCode>
    <ErrorMessage>Validation failed for required field</ErrorMessage>
    <Timestamp>2025-08-27T14:30:22Z</Timestamp>
    <RequestId>12345-67890-abcdef</RequestId>
</ErrorResponse>
```

## Message Formats

### Standard Request Format
```xml
<?xml version="1.0" encoding="UTF-8"?>
<DocumentMessage>
    <Header>
        <MessageID>{unique_id}</MessageID>
        <Timestamp>{current_timestamp}</Timestamp>
        <Source>
            <SystemName>CLIENT_SYSTEM</SystemName>
            <Version>1.0</Version>
        </Source>
        <Target>
            <SystemName>IBM_ACE</SystemName>
            <CountryCode>US</CountryCode>
        </Target>
    </Header>
    <Document>
        <DocumentType>
            <Code>{document_type_code}</Code>
            <n>{document_description}</n>
        </DocumentType>
        <EntityReference>
            <Type>{entity_type}</Type>
            <EntityID>{entity_id}</EntityID>
            <Reference Type="{reference_type}">{reference_value}</Reference>
        </EntityReference>
        <BusinessData>
            <!-- Business-specific data elements -->
        </BusinessData>
    </Document>
</DocumentMessage>
```

### Standard Response Format
```xml
<?xml version="1.0" encoding="UTF-8"?>
<ProcessingResponse>
    <Status>SUCCESS</Status>
    <MessageID>{original_message_id}</MessageID>
    <ProcessingTime>{processing_time_ms}ms</ProcessingTime>
    <Results>
        <ProcessedEntityID>{entity_id}</ProcessedEntityID>
        <EnrichmentApplied>true</EnrichmentApplied>
        <RoutingDecision>{routing_target}</RoutingDecision>
    </Results>
</ProcessingResponse>
```

## Business Entity Types
- **SHP**: Shipment entities
- **QBK**: Booking entities  
- **BRK**: Brokerage entities

## Reference Types
- **SSN**: Shipment Service Number
- **HouseBill**: House Bill Number
- **MasterBill**: Master Bill Number
- **BookingNumber**: Booking Reference Number
- **BrokerageID**: Brokerage Identifier

## Database Interactions
The message flows may perform database lookups for:
- Company code resolution
- Shipment ID lookups
- Document publication status
- Customs brokerage information
- eAdapter recipient configuration

## Performance Considerations
- **Typical Response Time**: < 2 seconds for standard messages
- **Large Message Processing**: < 10 seconds for messages > 1MB
- **Concurrent Processing**: Supports up to 100 concurrent requests
- **Rate Limiting**: No explicit limits (dependent on server capacity)

## Testing Guidelines
1. **Message IDs**: Use unique identifiers for each test
2. **Timestamps**: Use current timestamp format (ISO 8601)
3. **Entity IDs**: Use test prefixes to avoid conflicts
4. **Reference Values**: Use test data that won't interfere with production

## Support Information
For API questions or issues:
- Review IBM ACE server documentation
- Check server logs for detailed error information
- Contact the integration team for business logic questions
- Refer to the troubleshooting guide for common issues
