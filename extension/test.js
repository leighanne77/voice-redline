// Test OAuth flow
async function testOAuthFlow() {
  try {
    await initializeGoogleDocs();
    const doc = await gapi.client.docs.documents.get({
      documentId: 'DOCUMENT_ID'
    });
    console.log('Successfully accessed document:', doc);
  } catch (error) {
    console.error('OAuth test failed:', error);
  }
} 