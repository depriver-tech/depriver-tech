// Idempotent deployment step. Credentials stay in CI environment variables.
const account=process.env.CLOUDFLARE_ACCOUNT_ID;
const token=process.env.CLOUDFLARE_API_TOKEN;
if(!account||!token)throw new Error('Configure CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN.');
const root=`https://api.cloudflare.com/client/v4/accounts/${encodeURIComponent(account)}/r2/buckets`;
const headers={Authorization:`Bearer ${token}`,'Content-Type':'application/json'};
const check=await fetch(`${root}/depriver-docs-archive`,{headers});
if(check.ok){console.log('Archive bucket already exists.');}
else if(check.status===404){
 const created=await fetch(root,{method:'POST',headers,body:JSON.stringify({name:'depriver-docs-archive'})});
 if(!created.ok)throw new Error(`Archive bucket creation failed (${created.status}). Check R2 activation and token permissions.`);
 console.log('Private archive bucket created.');
}else throw new Error(`Archive bucket check failed (${check.status}). Check R2 activation and token permissions.`);
